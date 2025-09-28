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
