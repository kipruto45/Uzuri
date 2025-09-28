from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from .models import StudentProfile, FinanceRegistration, UnitRegistration, ExamCard, EXAM_TYPE_CHOICES
from .serializers import ExamCardSerializer
from django.db import transaction as db_transaction
from django.utils import timezone
from django.db import models

from my_profile.tasks import send_notification_email

class ExamCardViewSet(viewsets.ModelViewSet):
	@action(detail=True, methods=['get'])
	def download_pdf(self, request, pk=None):
        """
        Download/print exam card as branded PDF, increment reprint count, include QR/barcode, expiry check.
        """
        import io
        from django.http import FileResponse
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        card = self.get_object()
        # Expiry check
        if card.expiry_date and card.expiry_date < timezone.now().date():
            return Response({'error': 'Exam card expired.'}, status=status.HTTP_403_FORBIDDEN)
        # Branding assets (replace with actual logo/signature/stamp paths)
        university_name = "Uzuri University"
        logo_path = "static/branding/logo.png"  # Placeholder
        signature = "Registrar Signature"
        stamp = "Official Stamp"
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        p.setFont("Helvetica-Bold", 18)
        p.drawString(100, 800, university_name)
        p.setFont("Helvetica", 12)
        p.drawString(100, 780, f"Exam Card for {card.student.user.get_full_name()} ({card.student.user.student_number})")
        p.drawString(100, 760, f"Semester: {card.semester} | Type: {card.exam_type}")
        p.drawString(100, 740, f"Expiry: {card.expiry_date}")
        p.drawString(100, 720, f"Reprint #: {card.reprint_count + 1}")
        # QR/barcode placeholder
        p.drawString(100, 700, f"QR: {card.qr_code.url if card.qr_code else 'N/A'}")
        p.drawString(100, 680, f"Barcode: {card.barcode.url if card.barcode else 'N/A'}")
        # Units & schedule
        y = 660
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, y, "Units & Exam Schedule:")
        p.setFont("Helvetica", 12)
        for sched in card.exam_schedule:
            y -= 20
            p.drawString(120, y, f"{sched['unit_code']} - {sched['unit_title']} | {sched.get('date','')} {sched.get('time','')} @ {sched.get('venue','')}")
        # Branding
        p.drawString(100, y-40, signature)
        p.drawString(100, y-60, stamp)
        p.showPage()
        p.save()
        buffer.seek(0)
        # Track reprint
        card.reprint_count += 1
        card.download_history.append({'timestamp': str(timezone.now()), 'by': str(request.user)})
        card.save()
        return FileResponse(buffer, as_attachment=True, filename=f"exam_card_{card.student.user.student_number}_{card.semester}.pdf")

	queryset = ExamCard.objects.all()
	serializer_class = ExamCardSerializer
	permission_classes = [permissions.IsAuthenticated]

	@action(detail=False, methods=['post'])
	def generate(self, request):
		from payments.models import Payment, PaymentOption
		user = request.user
		profile = get_object_or_404(StudentProfile, user=user)
		semester = request.data.get('semester')
		exam_type = request.data.get('exam_type')
		supporting_document = request.FILES.get('supporting_document')
		approved_by_registrar = request.data.get('approved_by_registrar', False)
		# Restriction: Minimum tuition threshold
		tuition_option = PaymentOption.objects.filter(category="tuition").first()
		tuition_paid = Payment.objects.filter(user=user, status="successful", is_verified=True, is_non_refundable=False, method__name__in=["MPESA", "Airtel Money"]).aggregate(total=models.Sum("amount"))["total"] or 0
		tuition_required = 0
		if tuition_option:
			tuition_required = tuition_option.minimum_percentage_required / 100
		if tuition_option and tuition_required > 0 and tuition_paid < (tuition_option.minimum_percentage_required / 100) * getattr(tuition_option, 'amount', 0):
			# Business Rule: Auto-send alert if exam card not generated due to pending payments
			from notifications.models import Notification
			Notification.objects.create(
				user=user,
				message=f"Exam Card Blocked: You must pay at least {tuition_option.minimum_percentage_required}% of tuition fees before generating exam card.",
				type="exam_card_blocked",
			)
			return Response({'error': f'You must pay at least {tuition_option.minimum_percentage_required}% of tuition fees before generating exam card.'}, status=status.HTTP_403_FORBIDDEN)
		# Restriction: Outstanding balances
		outstanding = Payment.objects.filter(user=user, status__in=["pending", "failed"]).exists()
		if outstanding:
			# Business Rule: Auto-send alert if exam card not generated due to outstanding balances
			from notifications.models import Notification
			Notification.objects.create(
				user=user,
				message="Exam Card Blocked: You have outstanding balances. Settle all fees before generating exam card.",
				type="exam_card_blocked",
			)
			return Response({'error': 'You have outstanding balances. Settle all fees before generating exam card.'}, status=status.HTTP_403_FORBIDDEN)

		failed_units = []  # Ensure defined for all branches
		if exam_type == 'supplementary':
			# Restriction: Supplementary/special exam fees must be cleared
			supp_option = PaymentOption.objects.filter(category="examination").first()
			supp_paid = Payment.objects.filter(user=user, status="successful", is_verified=True, is_non_refundable=False, method__name__in=["MPESA", "Airtel Money"], paymentoption=supp_option).aggregate(total=models.Sum("amount"))["total"] or 0
			if supp_option and supp_paid < getattr(supp_option, 'amount', 0):
				return Response({'error': 'You must clear supplementary/special exam fees before generating this card.'}, status=status.HTTP_403_FORBIDDEN)
			# Get failed units from results (pseudo-code, replace with actual query)
			# Example: failed_units = [unit for unit in all_units if unit.grade == 'F']
			# For demo, use all units marked as 'supplementary' in registration
			unit_reg = UnitRegistration.objects.filter(student=profile, semester=semester, status='approved').first()
			units = unit_reg.items.filter(selected=True) if unit_reg else []
			failed_units = []
			for item in units:
				# Replace with actual grade check from results
				if hasattr(item.unit, 'is_failed') and item.unit.is_failed:
					failed_units.append({'code': item.unit.code, 'title': item.unit.name})
			if not failed_units:
				return Response({'error': 'No failed units found for supplementary exam card.'}, status=status.HTTP_400_BAD_REQUEST)
			# Finance check for each failed unit
			finance_ok = FinanceRegistration.objects.filter(student=profile, semester=semester, status='approved').exists()
			if not finance_ok:
				return Response({'error': 'Finance clearance for supplementary exam fee required.'}, status=status.HTTP_403_FORBIDDEN)
			# Check per-unit fee paid (pseudo-code)
			# TODO: Integrate with FinanceInvoice/FinanceRegistrationItem
			# Block if any failed unit fee not paid
			# Admin approval required
			if not approved_by_registrar:
				return Response({'error': 'Registrar approval required for supplementary exam card.'}, status=status.HTTP_403_FORBIDDEN)
			exam_schedule = [
				{'unit_code': u['code'], 'unit_title': u['title'], 'date': '2025-11-15', 'time': '14:00', 'venue': 'Supp Hall'} for u in failed_units
			]
		elif exam_type == 'special':
			# Special exam card requires manual approval and supporting document
			if not approved_by_registrar:
				return Response({'error': 'Registrar approval required for special exam card.'}, status=status.HTTP_403_FORBIDDEN)
			if not supporting_document:
				return Response({'error': 'Supporting document required for special exam card.'}, status=status.HTTP_400_BAD_REQUEST)
			# Custom exam assignment by admin (pseudo-code)
			custom_schedule = request.data.get('custom_schedule', [])
			exam_schedule = custom_schedule if custom_schedule else []
			# History tracking
			history = [{
				'action': 'special_approval',
				'by': str(user),
				'timestamp': str(timezone.now()),
				'reason': request.data.get('reason', '')
			}]
		else:
			# Ordinary/retake logic
			finance_ok = FinanceRegistration.objects.filter(student=profile, semester=semester, status='approved').exists()
			unit_ok = UnitRegistration.objects.filter(student=profile, semester=semester, status='approved').exists()
			if not (finance_ok and unit_ok):
				return Response({'error': 'You are not eligible to generate an exam card. Please complete finance and unit registration first.'}, status=status.HTTP_403_FORBIDDEN)
			unit_reg = UnitRegistration.objects.filter(student=profile, semester=semester, status='approved').first()
			units = unit_reg.items.filter(selected=True) if unit_reg else []
			exam_schedule = [
				{'unit_code': item.unit.code, 'unit_title': item.unit.name, 'date': '2025-11-10', 'time': '09:00', 'venue': 'Main Hall'} for item in units
			]

		# Block check
		if ExamCard.objects.filter(student=profile, semester=semester, is_blocked=True).exists():
			return Response({'error': 'You are blocked from generating an exam card. Contact registrar.'}, status=status.HTTP_403_FORBIDDEN)

		# Generate QR/barcode (placeholder)
		qr_data = f"{profile.user.id}-{semester}-{exam_type}"  # Use a real QR library in production
		barcode_data = f"{profile.user.id}-{semester}"  # Use a real barcode library in production

		# Create card
		with db_transaction.atomic():
			card = ExamCard.objects.create(
				student=profile,
				semester=semester,
				exam_type=exam_type,
				expiry_date=timezone.now().date() + timezone.timedelta(days=30),
				approved_by_registrar=approved_by_registrar,
				supporting_document=supporting_document if exam_type == 'special' else None,
				failed_units=failed_units if exam_type == 'supplementary' else [],
				exam_schedule=exam_schedule,
				history=history if exam_type == 'special' else [],
				finance_confirmed=finance_ok,
			)
			# Track reprints
			card.reprint_count = 0
			card.save()
		# Notification triggers (must be before return)
		if exam_type == 'special':
			send_notification_email.delay(
				profile.user.email,
				'Special Exam Card Approved',
				'Your special exam card has been approved and is now available.',
				event_type='success',
				in_app=True,
				sms=True
			)
		elif exam_type == 'supplementary':
			send_notification_email.delay(
				profile.user.email,
				'Supplementary Exam Card Ready',
				'Your supplementary exam card is now available.',
				event_type='info',
				in_app=True,
				sms=True
			)
		else:
			send_notification_email.delay(
				profile.user.email,
				'Exam Card Generated',
				'Your exam card is now available.',
				event_type='info',
				in_app=True,
				sms=False
			)
		return Response({
			'card': ExamCardSerializer(card).data,
			'student_details': {
				'name': profile.user.get_full_name(),
				'student_number': getattr(profile, 'student_number', ''),
				'program': profile.program,
				'year': profile.year_of_study,
				'semester': semester,
			},
			'units': card.failed_units if exam_type == 'supplementary' else [{'code': item.unit.code, 'title': item.unit.name} for item in units],
			'exam_schedule': exam_schedule,
			'qr_data': qr_data,
			'barcode_data': barcode_data,
			'reprint_count': card.reprint_count,
		}, status=status.HTTP_201_CREATED)
				in_app=True,
				sms=True
			)
		elif exam_type == 'supplementary':
			send_notification_email.delay(
				profile.user.email,
				'Supplementary Exam Card Ready',
				'Your supplementary exam card is now available.',
				event_type='info',
				in_app=True,
				sms=True
			)
		else:
			send_notification_email.delay(
				profile.user.email,
				'Exam Card Generated',
				'Your exam card is now available.',
				event_type='info',
				in_app=True,
				sms=False
			)
		return Response({
			'card': ExamCardSerializer(card).data,
			'student_details': {
				'name': profile.user.get_full_name(),
				'student_number': getattr(profile, 'student_number', ''),
				'program': profile.program,
				'year': profile.year_of_study,
				'semester': semester,
			},
			'units': card.failed_units if exam_type == 'supplementary' else [{'code': item.unit.code, 'title': item.unit.name} for item in units],
			'exam_schedule': exam_schedule,
			'qr_data': qr_data,
			'barcode_data': barcode_data,
			'reprint_count': card.reprint_count,
		}, status=status.HTTP_201_CREATED)
		return Response({
			'card': ExamCardSerializer(card).data,
			'student_details': {
				'name': profile.user.get_full_name(),
				'student_number': getattr(profile, 'student_number', ''),
				'program': profile.program,
				'year': profile.year_of_study,
				'semester': semester,
			},
			'units': card.failed_units if exam_type == 'supplementary' else [{'code': item.unit.code, 'title': item.unit.name} for item in units],
			'exam_schedule': exam_schedule,
			'qr_data': qr_data,
			'barcode_data': barcode_data,
			'reprint_count': card.reprint_count,
		}, status=status.HTTP_201_CREATED)
