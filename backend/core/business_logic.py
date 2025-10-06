from .models import *
from django.utils import timezone

# Example: Student registration logic

def register_unit(student_profile, unit):
    # Check if already registered
    if Registration.objects.filter(student=student_profile, unit=unit).exists():
        return False, 'Already registered for this unit.'
    # Check prerequisites, capacity, etc. (placeholder)
    # ...
    Registration.objects.create(student=student_profile, unit=unit, date_registered=timezone.now(), status='pending')
    return True, 'Registration successful.'

# Example: Finance logic

def pay_invoice(student_profile, invoice, amount, method, reference):
    if invoice.status == 'paid':
        return False, 'Invoice already paid.'
    if amount < invoice.amount:
        return False, 'Insufficient payment.'
    transaction = Transaction.objects.create(invoice=invoice, amount=amount, method=method, reference=reference, date=timezone.now())
    invoice.status = 'paid'
    invoice.save()
    Receipt.objects.create(transaction=transaction, issued_at=timezone.now())
    return True, 'Payment successful.'

# Example: Admin logic

def approve_student_admission(student_profile):
    # Placeholder for approval workflow
    student_profile.status = 'admitted'
    student_profile.save()
    return True, 'Admission approved.'

# Example: Permissions utility

def has_role(user, role_name):
    return user.role and user.role.name == role_name
