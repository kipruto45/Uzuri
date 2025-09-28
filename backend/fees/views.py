from django.http import FileResponse
from django.conf import settings
from .tasks import generate_receipt_pdf_task, send_notification_task
from .integration import initiate_mpesa_stk_push, MpesaWebhookView, record_manual_payment, send_email_notification, send_sms_notification



from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, throttle_classes
from rest_framework.response import Response
from .models import Invoice, Transaction, Receipt, FeeStructure, Scholarship, AuditTrail
from rest_framework.throttling import UserRateThrottle
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import InvoiceSerializer, TransactionSerializer, ReceiptSerializer, FeeStructureSerializer, ScholarshipSerializer, AuditTrailSerializer
class ScholarshipViewSet(viewsets.ModelViewSet):
    serializer_class = ScholarshipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'studentprofile'):
            return Scholarship.objects.filter(student__user=self.request.user)
        return Scholarship.objects.all()

class AuditTrailViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AuditTrailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AuditTrail.objects.all()
from my_profile.models import StudentProfile
from django.shortcuts import get_object_or_404
from django.db import models


# Permission: Only allow students to access their own records
class IsStudentSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return hasattr(obj, 'student') and getattr(obj.student, 'user', None) == request.user

class InvoiceViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['post'], url_path='bulk-create')
    def bulk_create(self, request):
        serializer = InvoiceSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        Invoice.objects.bulk_create([Invoice(**item) for item in serializer.validated_data])
        return Response({'detail': 'Bulk invoices created.'}, status=201)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['student', 'status', 'due_date']
    search_fields = ['student__user__username', 'student__user__email', 'status']
    ordering_fields = ['due_date', 'amount', 'status']

    @action(detail=False, methods=['get'], url_path='statement')
    def statement(self, request):
        try:
            profile = get_object_or_404(StudentProfile, user=request.user)
            invoices = Invoice.objects.filter(student=profile)
            transactions = Transaction.objects.filter(student=profile)
            total_invoiced = invoices.aggregate(models.Sum('amount'))['amount__sum'] or 0
            total_paid = transactions.filter(status='success').aggregate(models.Sum('amount'))['amount__sum'] or 0
            balance = total_invoiced - total_paid
            return Response({
                'invoices': InvoiceSerializer(invoices, many=True).data,
                'transactions': TransactionSerializer(transactions, many=True).data,
                'total_invoiced': total_invoiced,
                'total_paid': total_paid,
                'balance': balance
            })
        except Exception as e:
            return Response({'detail': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudentSelf]

    def get_queryset(self):
        profile = get_object_or_404(StudentProfile, user=self.request.user)
        return Invoice.objects.filter(student=profile)

class TransactionViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['post'], url_path='bulk-create')
    def bulk_create(self, request):
        serializer = TransactionSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        Transaction.objects.bulk_create([Transaction(**item) for item in serializer.validated_data])
        return Response({'detail': 'Bulk transactions created.'}, status=201)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['student', 'invoice', 'status', 'method']
    search_fields = ['student__user__username', 'invoice__reference', 'status', 'method', 'reference']
    ordering_fields = ['created_at', 'amount', 'status']

    @swagger_auto_schema(
        method='post',
        operation_description="Initiate a payment for an invoice.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['invoice_id', 'amount', 'method'],
            properties={
                'invoice_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                'method': openapi.Schema(type=openapi.TYPE_STRING, enum=['mpesa', 'manual']),
                'reference': openapi.Schema(type=openapi.TYPE_STRING),
                'phone': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={200: openapi.Response('Payment response')}
    )
    @action(detail=False, methods=['post'], url_path='pay')
    @throttle_classes([UserRateThrottle])
    def pay(self, request):
        try:
            invoice_id = request.data.get('invoice_id')
            amount = request.data.get('amount')
            method = request.data.get('method')
            reference = request.data.get('reference', '')
            phone = request.data.get('phone', None)
            if not invoice_id or not amount or not method:
                return Response({'detail': 'invoice_id, amount, and method are required.'}, status=400)
            try:
                amount = float(amount)
                if amount <= 0:
                    raise ValueError
            except Exception:
                return Response({'detail': 'Amount must be a positive number.'}, status=400)
            if method == 'mpesa' and (not phone or len(str(phone)) < 10):
                return Response({'detail': 'Valid phone number required for M-Pesa.'}, status=400)
            invoice = get_object_or_404(Invoice, id=invoice_id, student__user=request.user)
            AuditTrail.objects.create(user=request.user, action='initiate_payment', model='Transaction', object_id=reference, changes=f'before: {invoice.status}')
            if method == 'mpesa':
                resp = initiate_mpesa_stk_push(phone, amount, reference)
                transaction = Transaction.objects.create(
                    student=invoice.student,
                    invoice=invoice,
                    amount=amount,
                    method=method,
                    reference=reference,
                    status='pending',
                )
                send_notification_task.delay(invoice.student.user.id, f'Payment initiated via M-Pesa. Await confirmation.')
                AuditTrail.objects.create(user=request.user, action='payment_created', model='Transaction', object_id=transaction.id, changes=f'after: pending')
                return Response({'transaction_id': transaction.id, 'status': 'pending', 'gateway': resp})
            elif method == 'manual':
                tx = record_manual_payment(invoice_id, amount, reference, request.user)
                AuditTrail.objects.create(user=request.user, action='manual_payment', model='Transaction', object_id=tx.id, changes=f'after: success')
                return Response({'transaction_id': tx.id, 'status': 'success'})
            return Response({'detail': 'Unsupported payment method.'}, status=400)
        except Exception as e:
            return Response({'detail': f'An error occurred: {str(e)}'}, status=500)
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudentSelf]

    def get_queryset(self):
        profile = get_object_or_404(StudentProfile, user=self.request.user)
        return Transaction.objects.filter(student=profile)

class ReceiptViewSet(viewsets.ReadOnlyModelViewSet):
    @action(detail=True, methods=['get'], url_path='download')
    def download(self, request, pk=None):
        receipt = self.get_object()
        if not receipt.pdf_file:
            return Response({'detail': 'Receipt not available.'}, status=404)
        return FileResponse(receipt.pdf_file, as_attachment=True, filename=f'receipt_{receipt.id}.pdf')
    serializer_class = ReceiptSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudentSelf]

    def get_queryset(self):
        profile = get_object_or_404(StudentProfile, user=self.request.user)
        return Receipt.objects.filter(transaction__student=profile)

class FeeStructureViewSet(viewsets.ModelViewSet):
    # Finance/Admin endpoints for bulk invoice creation, manual payment, and reports can be added here
    @action(detail=False, methods=['post'], url_path='generate-invoices')
    def generate_invoices(self, request):
        # Example: Auto-generate invoices for all students in a program/year/semester
        program = request.data.get('program')
        year = request.data.get('year')
        semester = request.data.get('semester')
        amount = request.data.get('amount')
        # ... logic to get students and create invoices ...
        # send_notification_task.delay(...)
        return Response({'detail': 'Invoices generated (stub).'}, status=201)
    serializer_class = FeeStructureSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FeeStructure.objects.all()



# Create your views here.
