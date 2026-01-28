from rest_framework.permissions import BasePermission


class IsProjectOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsTaskEditor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            obj.assigned_to == request.user
            or obj.project.owner == request.user
        )