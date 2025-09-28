from celery import shared_task
from django.utils import timezone
from exam_card.models import ExamCard, ExamCardEvent
from finance_registration.models import FinanceRegistration
from unit_registration.models import UnitRegistration
from my_profile.models import StudentProfile

@shared_task
def auto_generate_exam_cards():
    # Automatically generate exam cards for eligible students
    today = timezone.now().date()
    for profile in StudentProfile.objects.all():
        semester = '2025-2'  # Replace with dynamic semester logic
        finance_ok = FinanceRegistration.objects.filter(student=profile, semester=semester, status='approved').exists()
        unit_ok = UnitRegistration.objects.filter(student=profile, semester=semester, status='approved').exists()
        if finance_ok and unit_ok:
            if not ExamCard.objects.filter(student=profile, semester=semester).exists():
                card = ExamCard.objects.create(student=profile, semester=semester, exam_type='ordinary', expiry_date=today + timezone.timedelta(days=30))
                ExamCardEvent.objects.create(card=card, event_type='generated', user=profile, details='Auto-generated exam card.')

@shared_task
def send_exam_card_notifications():
    # Notify students of card availability and expiry
    today = timezone.now().date()
    for card in ExamCard.objects.filter(expiry_date__gte=today):
        # from notifications.models import Notification
        # Notification.objects.create(user=card.student.user, message='Your exam card is available.', type='exam_card')
        pass
    for card in ExamCard.objects.filter(expiry_date__lte=today):
        # Notification.objects.create(user=card.student.user, message='Your exam card has expired.', type='exam_card')
        pass
