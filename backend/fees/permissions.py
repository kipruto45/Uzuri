from rest_framework import permissions

class IsFinanceStaff(permissions.BasePermission):
    """Allow access only to finance staff or superusers."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_superuser or getattr(request.user, 'is_finance_staff', False))

class IsStudentSelf(permissions.BasePermission):
    """Allow students to access only their own records."""
    def has_object_permission(self, request, view, obj):
        return hasattr(obj, 'student') and getattr(obj.student, 'user', None) == request.user
