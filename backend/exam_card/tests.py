
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import ExamCard

class ExamCardModuleTests(TestCase):
	def setUp(self):
		User = get_user_model()
		self.user = User.objects.create_user(email='student1@example.com', password='testpass')
		self.card = ExamCard.objects.create(student=self.user, card_type='regular', file='exam_cards/test.pdf')

	def test_exam_card_creation(self):
		self.assertEqual(self.card.card_type, 'regular')
		self.assertTrue(self.card.file)
