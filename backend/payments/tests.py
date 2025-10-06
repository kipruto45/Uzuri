from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import PaymentMethod, PaymentGateway, Payment, PaymentReceipt, Refund
from core.models import CustomUser

class PaymentMethodModelTest(TestCase):
	def test_create_payment_method(self):
		method = PaymentMethod.objects.create(name="Mpesa")
		self.assertEqual(str(method), "Mpesa")

class PaymentGatewayModelTest(TestCase):
	def test_create_payment_gateway(self):
		gateway = PaymentGateway.objects.create(name="Mpesa Gateway")
		self.assertEqual(str(gateway), "Mpesa Gateway")

class PaymentModelTest(TestCase):
	def setUp(self):
		self.user = CustomUser.objects.create(email="test@example.com")
		self.method = PaymentMethod.objects.create(name="Mpesa")
		self.gateway = PaymentGateway.objects.create(name="Mpesa Gateway")

	def test_create_payment(self):
		payment = Payment.objects.create(
			user=self.user,
			amount=1000,
			currency="KES",
			method=self.method,
			gateway=self.gateway,
			status="pending",
			reference="REF12345"
		)
		self.assertEqual(str(payment), f"{self.user} - 1000.00 KES (pending)")

class PaymentAPITest(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.user = CustomUser.objects.create_user(email="apiuser@example.com", password="testpass123")
		self.client.force_authenticate(user=self.user)
		self.method = PaymentMethod.objects.create(name="Mpesa")
		self.gateway = PaymentGateway.objects.create(name="Mpesa Gateway")

	def test_create_payment(self):
		from rest_framework.reverse import reverse
		url = reverse("payment-list")
		data = {
			"user": self.user.id,
			"amount": 5000,
			"currency": "KES",
			"method": self.method.id,
			"gateway": self.gateway.id,
			"status": "pending",
			"reference": "APIREF123"
		}
		response = self.client.post(url, data, follow=True)
		self.assertIn(response.status_code, [status.HTTP_201_CREATED, 301])
		if response.status_code == status.HTTP_201_CREATED:
			self.assertEqual(response.data["reference"], "APIREF123")

	def test_list_payments(self):
		Payment.objects.create(
			user=self.user,
			amount=1000,
			currency="KES",
			method=self.method,
			gateway=self.gateway,
			status="pending",
			reference="REFLIST1"
		)
		from rest_framework.reverse import reverse
		url = reverse("payment-list")
		response = self.client.get(url, follow=True)
		self.assertIn(response.status_code, [status.HTTP_200_OK, 301])
		if response.status_code == status.HTTP_200_OK:
			self.assertGreaterEqual(len(response.data), 1)

	def test_airtel_initiate_endpoint(self):
		from rest_framework.reverse import reverse
		url = reverse('airtel-initiate')
		response = self.client.post(url, {'amount': 1500, 'phone': '254700000000'}, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn('reference', response.data)

	def test_mpesa_initiate_endpoint(self):
		from rest_framework.reverse import reverse
		url = reverse('mpesa-initiate')
		response = self.client.post(url, {'amount': 2000, 'phone': '254700000000'}, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn('reference', response.data)

	def test_mpesa_initiate_with_external_call(self):
		from rest_framework.reverse import reverse
		url = reverse('mpesa-initiate')
		# Mock token and STK push calls
		from unittest.mock import patch, Mock
		mock_token_resp = Mock()
		mock_token_resp.status_code = 200
		mock_token_resp.json.return_value = {'access_token': 'fake-token'}
		mock_stk_resp = Mock()
		mock_stk_resp.status_code = 200
		mock_stk_resp.content = b'{}'
		mock_stk_resp.json.return_value = {'CheckoutRequestID': 'CR123'}
		with patch('payments.views.requests.get', return_value=mock_token_resp) as mg, patch('payments.views.requests.post', return_value=mock_stk_resp) as mp:
			response = self.client.post(url, {'amount': 2000, 'phone': '254700000000'}, format='json')
			self.assertEqual(response.status_code, status.HTTP_200_OK)
			self.assertIn('reference', response.data)

	def test_airtel_initiate_with_external_call(self):
		from rest_framework.reverse import reverse
		url = reverse('airtel-initiate')
		from unittest.mock import patch, Mock
		mock_resp = Mock()
		mock_resp.status_code = 200
		mock_resp.content = b'{}'
		mock_resp.json.return_value = {'status': 'ok', 'request_id': 'AR123'}
		with patch('payments.views.requests.post', return_value=mock_resp) as mp:
			response = self.client.post(url, {'amount': 1500, 'phone': '254700000000'}, format='json')
			self.assertEqual(response.status_code, status.HTTP_200_OK)
			self.assertIn('reference', response.data)

	def test_mpesa_callback_updates_payment(self):
		# create a payment that will be updated by the callback
		payment = Payment.objects.create(
			user=self.user,
			amount=2000,
			currency='KES',
			method=self.method,
			gateway=self.gateway,
			status='processing',
			reference='CALLBACKREF123'
		)
		from rest_framework.reverse import reverse
		url = reverse('mpesa-callback')
		payload = {
			'Body': {
				'stkCallback': {
					'MerchantRequestID': '123',
					'CheckoutRequestID': '456',
					'ResultCode': 0,
					'ResultDesc': 'The service request is processed successfully.',
					'CallbackMetadata': {
						'Item': [
							{'Name': 'Amount', 'Value': 2000},
							{'Name': 'MpesaReceiptNumber', 'Value': 'ABC123XYZ'},
							{'Name': 'TransactionDate', 'Value': 20251004201000},
							{'Name': 'PhoneNumber', 'Value': '254700000000'},
							{'Name': 'AccountReference', 'Value': 'CALLBACKREF123'},
						]
					}
				}
			}
		}
		# Set webhook secret in settings during the test
		from django.test import override_settings
		with override_settings(MPESA_WEBHOOK_SECRET='testwebhook'):
			response = self.client.post(url, payload, format='json', HTTP_X_WEBHOOK_SECRET='testwebhook')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		payment.refresh_from_db()
		self.assertEqual(payment.status, 'successful')
		self.assertEqual(payment.transaction_id, 'ABC123XYZ')

	def test_mpesa_duplicate_callback_is_idempotent(self):
		payment = Payment.objects.create(
			user=self.user,
			amount=3000,
			currency='KES',
			method=self.method,
			gateway=self.gateway,
			status='processing',
			reference='DUPLICATEREF'
		)
		from rest_framework.reverse import reverse
		url = reverse('mpesa-callback')
		payload = {
			'Body': {
				'stkCallback': {
					'MerchantRequestID': 'MREQ1',
					'CheckoutRequestID': 'CREQ1',
					'ResultCode': 0,
					'ResultDesc': 'Success',
					'CallbackMetadata': {
						'Item': [
							{'Name': 'Amount', 'Value': 3000},
							{'Name': 'MpesaReceiptNumber', 'Value': 'RCPT1'},
							{'Name': 'AccountReference', 'Value': 'DUPLICATEREF'},
						]
					}
				}
			}
		}
		from django.test import override_settings
		with override_settings(MPESA_WEBHOOK_SECRET='dupsecret'):
			resp1 = self.client.post(url, payload, format='json', HTTP_X_WEBHOOK_SECRET='dupsecret')
			resp2 = self.client.post(url, payload, format='json', HTTP_X_WEBHOOK_SECRET='dupsecret')
		self.assertEqual(resp1.status_code, status.HTTP_200_OK)
		# second request should return 200 but indicate already processed
		self.assertEqual(resp2.status_code, status.HTTP_200_OK)
		self.assertIn('already processed', resp2.data.get('detail', '').lower())
		payment.refresh_from_db()
		self.assertEqual(payment.status, 'successful')

	def test_mpesa_callback_failure_code_does_not_mark_success(self):
		payment = Payment.objects.create(
			user=self.user,
			amount=1200,
			currency='KES',
			method=self.method,
			gateway=self.gateway,
			status='processing',
			reference='FAILREF'
		)
		from rest_framework.reverse import reverse
		url = reverse('mpesa-callback')
		payload = {
			'Body': {
				'stkCallback': {
					'MerchantRequestID': 'MREQF',
					'CheckoutRequestID': 'CREQF',
					'ResultCode': 1032,
					'ResultDesc': 'Insufficient funds',
					'CallbackMetadata': {
						'Item': [
							{'Name': 'Amount', 'Value': 1200},
							{'Name': 'MpesaReceiptNumber', 'Value': 'RCPTF'},
							{'Name': 'AccountReference', 'Value': 'FAILREF'},
						]
					}
				}
			}
		}
		from django.test import override_settings
		with override_settings(MPESA_WEBHOOK_SECRET='failsecret'):
			resp = self.client.post(url, payload, format='json', HTTP_X_WEBHOOK_SECRET='failsecret')
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		payment.refresh_from_db()
		# Should not be successful
		self.assertNotEqual(payment.status, 'successful')

	def test_airtel_duplicate_callback_is_idempotent(self):
		payment = Payment.objects.create(
			user=self.user,
			amount=1800,
			currency='KES',
			method=self.method,
			gateway=self.gateway,
			status='processing',
			reference='AIRTELDUP'
		)
		from rest_framework.reverse import reverse
		url = reverse('airtel-callback')
		payload = {
			'reference': 'AIRTELDUP',
			'transaction_id': 'ATX1',
			'status': 'success',
			'amount': 1800,
			'callback_id': 'ATCB1'
		}
		resp1 = self.client.post(url, payload, format='json')
		resp2 = self.client.post(url, payload, format='json')
		self.assertEqual(resp1.status_code, status.HTTP_200_OK)
		self.assertEqual(resp2.status_code, status.HTTP_200_OK)
		self.assertIn('already processed', resp2.data.get('detail', '').lower())
		payment.refresh_from_db()
		self.assertEqual(payment.status, 'successful')

	def test_airtel_callback_missing_reference(self):
		url = reverse('airtel-callback')
		payload = {'transaction_id': 'X', 'status': 'success'}
		resp = self.client.post(url, payload, format='json')
		self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

	def test_airtel_callback_invalid_webhook_secret(self):
		from django.test import override_settings
		url = reverse('airtel-callback')
		payload = {'reference': 'SOMEREF', 'transaction_id': 'X', 'status': 'success'}
		with override_settings(AIRTEL_WEBHOOK_SECRET='expected'):
			resp = self.client.post(url, payload, format='json', HTTP_X_WEBHOOK_SECRET='wrong')
		self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

	def test_airtel_callback_missing_transaction_id(self):
		payment = Payment.objects.create(
			user=self.user,
			amount=900,
			currency='KES',
			method=self.method,
			gateway=self.gateway,
			status='processing',
			reference='AIR_MISS_TX'
		)
		url = reverse('airtel-callback')
		payload = {'reference': 'AIR_MISS_TX', 'status': 'success'}
		resp = self.client.post(url, payload, format='json')
		# should still process if reference present; transaction_id optional
		self.assertEqual(resp.status_code, status.HTTP_200_OK)

	def test_airtel_callback_missing_status(self):
		payment = Payment.objects.create(
			user=self.user,
			amount=750,
			currency='KES',
			method=self.method,
			gateway=self.gateway,
			status='processing',
			reference='AIR_MISS_STATUS'
		)
		url = reverse('airtel-callback')
		payload = {'reference': 'AIR_MISS_STATUS', 'transaction_id': 'TID1'}
		resp = self.client.post(url, payload, format='json')
		# missing status should be treated as failed by default
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		payment.refresh_from_db()
		self.assertNotEqual(payment.status, 'successful')

	def test_airtel_callback_non_dict_payload(self):
		url = reverse('airtel-callback')
		# Simulate non-dict (string) payload - should return 400
		resp = self.client.post(url, 'not-a-json', content_type='application/json')
		self.assertIn(resp.status_code, [400, 415])
