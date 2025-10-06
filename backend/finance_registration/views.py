from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

# Student dashboard API: returns finance status, invoices, payment history, and registration summary
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def finance_dashboard(request):
	user = request.user
	from my_profile.models import StudentProfile
	profile = StudentProfile.objects.filter(user=user).first()
	if not profile:
		return Response({'error': 'Student profile not found.'}, status=404)
	registrations = FinanceRegistration.objects.filter(student=profile).order_by('-created_at')
	invoices = FinanceInvoice.objects.filter(registration__student=profile).order_by('-updated_at')
	invoice_data = FinanceInvoiceSerializer(invoices, many=True).data
	reg_data = FinanceRegistrationSerializer(registrations, many=True).data
	total_due = sum([float(inv['total_amount']) - float(inv['paid_amount']) for inv in invoice_data])
	status = 'clear' if total_due == 0 else 'pending'
	return Response({
		'student': profile.user.email,
		'semester': registrations.first().semester if registrations.exists() else None,
		'registrations': reg_data,
		'invoices': invoice_data,
		'total_due': total_due,
		'status': status,
		'last_updated': timezone.now(),
	})
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import FinanceCategory, FinanceRegistration, FinanceRegistrationItem, FinanceInvoice
from .serializers import FinanceCategorySerializer, FinanceRegistrationSerializer, FinanceInvoiceSerializer
from my_profile.models import StudentProfile
from django.shortcuts import get_object_or_404
from django.db import transaction as db_transaction

class FinanceCategoryViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = FinanceCategory.objects.filter(is_active=True)
	serializer_class = FinanceCategorySerializer
	permission_classes = [permissions.IsAuthenticated]

class FinanceRegistrationViewSet(viewsets.ModelViewSet):
	queryset = FinanceRegistration.objects.all()
	serializer_class = FinanceRegistrationSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_staff:
			return FinanceRegistration.objects.all()
		profile = get_object_or_404(StudentProfile, user=user)
		return FinanceRegistration.objects.filter(student=profile)

	def create(self, request, *args, **kwargs):
		user = request.user
		profile = get_object_or_404(StudentProfile, user=user)
		data = request.data.copy()
		data['student'] = profile.id
		serializer = self.get_serializer(data=data)
		serializer.is_valid(raise_exception=True)
		with db_transaction.atomic():
			registration = serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)

	@action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
	def approve(self, request, pk=None):
		registration = self.get_object()
		registration.status = 'approved'
		registration.approved_by = request.user
		registration.approved_at = timezone.now()
		registration.save()
		return Response({'detail': 'Finance registration approved.'})

class FinanceInvoiceViewSet(viewsets.ModelViewSet):
	queryset = FinanceInvoice.objects.all()
	serializer_class = FinanceInvoiceSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_staff:
			return FinanceInvoice.objects.all()
		profile = get_object_or_404(StudentProfile, user=user)
		return FinanceInvoice.objects.filter(registration__student=profile)

	@action(detail=True, methods=['post'])
	def pay(self, request, pk=None):
		from decimal import Decimal
		invoice = self.get_object()
		amount = request.data.get('amount')
		try:
			amount = Decimal(str(amount))
		except (TypeError, ValueError, ArithmeticError):
			return Response({'error': 'Amount must be a valid number.'}, status=400)
		if amount <= 0:
			return Response({'error': 'Amount must be positive.'}, status=400)
		invoice.paid_amount += amount
		if invoice.paid_amount >= invoice.total_amount:
			invoice.status = 'paid'
			invoice.paid_amount = invoice.total_amount
		elif invoice.paid_amount > 0:
			invoice.status = 'partial'
		invoice.save()
		return Response(self.get_serializer(invoice).data)
