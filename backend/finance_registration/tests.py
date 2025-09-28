from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from my_profile.models import StudentProfile
from .models import FinanceCategory, FinanceRegistration, FinanceRegistrationItem, FinanceInvoice
from django.contrib.auth import get_user_model

User = get_user_model()

class FinanceRegistrationFlowTest(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(email='student@example.com', password='pass', first_name='Test', last_name='Student')
		self.profile = StudentProfile.objects.create(
			user=self.user,
			program='BSc CS',
			year_of_study=1,
			dob='2000-01-01',
			gender='M',
			phone='0712345678',
			address='123 Main St',
			emergency_contact='Parent',
		)
		self.category1 = FinanceCategory.objects.create(name='Tuition', default_amount=50000)
		self.category2 = FinanceCategory.objects.create(name='Accommodation', default_amount=20000)
		login_url = reverse('auth-login')
		resp = self.client.post(login_url, {'email': 'student@example.com', 'password': 'pass'}, format='json', follow=True)
		assert resp.status_code in [200, 201], f"Login failed: {resp.data}"
		token = resp.data.get('access')
		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

	def test_finance_registration_and_invoice(self):
		reg_url = reverse('finance-registration-list')
		data = {
			'semester': '2025-1',
			'items': [
				{'category_id': self.category1.id, 'amount': 50000, 'selected': True},
				{'category_id': self.category2.id, 'amount': 20000, 'selected': True},
			]
		}
		resp = self.client.post(reg_url, data, format='json', follow=True)
		self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
		reg_id = resp.data['id']
		invoice = FinanceInvoice.objects.create(registration_id=reg_id, total_amount=70000, due_date='2025-10-01')
		inv_url = reverse('finance-invoice-detail', args=[invoice.id])
		pay_resp = self.client.post(inv_url + 'pay/', {'amount': 70000}, format='json')
		self.assertEqual(pay_resp.status_code, status.HTTP_200_OK)
		self.assertEqual(pay_resp.data['status'], 'paid')
