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


class HasRole(permissions.BasePermission):
    """Generic permission that checks if the user has one of the required roles.

    Views can set `required_roles = ['Registrar', 'Finance Staff']` attribute.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        required = getattr(view, 'required_roles', None)
        if not required:
            return True
        # user.role is a string on CustomUser
        user_role = getattr(request.user, 'role', None)
        if not user_role:
            return False
        if isinstance(required, (list, tuple)):
            return user_role in required
        return user_role == required
