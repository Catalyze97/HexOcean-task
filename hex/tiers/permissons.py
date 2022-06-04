"""Permission class for tiers."""
from rest_framework import permissions


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):

        if view.action == ['POST']:
            return request.user.is_authenticated and request.user.is_staff
        elif view.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy']:
            return request.user.is_authenticated
        else:
            return False
