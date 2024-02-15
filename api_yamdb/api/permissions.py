from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    """Анонимам можно только читать, все CRUD операции доступны админу."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.is_staff
        )
