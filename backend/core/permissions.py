from rest_framework import permissions


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'is_student') and request.user.is_student()

class IsLecturer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user.role, 'name', None) == 'Lecturer'

class IsFinanceStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user.role, 'name', None) == 'Finance Staff'

class IsRegistrar(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user.role, 'name', None) == 'Registrar'

class IsSystemAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user.role, 'name', None) == 'System Administrator'

class IsParentGuardian(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user.role, 'name', None) == 'Parent/Guardian'

class IsGuest(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user.role, 'name', None) == 'Guest'

class IsSupportStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user.role, 'name', None) == 'Support Staff'
