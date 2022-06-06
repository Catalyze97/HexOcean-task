"""Permission class for tiers."""
from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    """Permissions for normal users,
        forbidding create, update and destroy tier."""
    def has_permission(self, request, view):

        if view.action == ['POST', 'destroy', 'update', 'partial_update']:
            return request.user.is_authenticated and request.user.is_staff
        elif view.action in ['list', 'retrieve']:
            return request.user.is_authenticated
        else:
            return False
