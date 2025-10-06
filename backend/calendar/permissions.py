from rest_framework import permissions

class IsEventOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.created_by == request.user or request.user in obj.shared_with.all()

class IsLecturerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or getattr(request.user, 'is_lecturer', False)
