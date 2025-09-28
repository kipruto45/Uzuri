from rest_framework import permissions

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'is_student') and request.user.is_student

class IsLecturer(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'is_lecturer') and request.user.is_lecturer

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or getattr(obj, 'student', None) == request.user

class IsEnrolledOrLecturer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow if user is enrolled in the unit or is the lecturer
        if hasattr(obj, 'unit'):
            if hasattr(request.user, 'is_lecturer') and request.user.is_lecturer:
                return obj.unit.lecturer == request.user
            if hasattr(request.user, 'is_student') and request.user.is_student:
                return obj.unit.enrollment_set.filter(student=request.user, status='active').exists()
        return False

class IsGroupMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.members.all()

class IsGuardianOrStudent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'guardian'):
            return obj.guardian.user == request.user or obj.student == request.user
        return False

class IsMarketplaceOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.uploaded_by == request.user

class IsAuditLogOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsDashboardWidgetOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.student == request.user
