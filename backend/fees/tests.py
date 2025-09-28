
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Invoice, Transaction

class FeesModuleTests(TestCase):
	def setUp(self):
		User = get_user_model()
		self.user = User.objects.create_user(email='student1@example.com', password='testpass')
		self.invoice = Invoice.objects.create(student=self.user, amount=1000, due_date='2025-10-01', status='unpaid')

	def test_invoice_creation(self):
		self.assertEqual(self.invoice.amount, 1000)
		self.assertEqual(self.invoice.status, 'unpaid')

	def test_payment_workflow(self):
		tx = Transaction.objects.create(student=self.user, invoice=self.invoice, amount=1000, status='successful')
		self.assertEqual(tx.status, 'successful')
