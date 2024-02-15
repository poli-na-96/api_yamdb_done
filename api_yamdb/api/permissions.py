from rest_framework import permissions


class AnonimReadOnly(permissions.BasePermission):
    """может просматривать описания произведений,
    читать отзывы и комментарии."""
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class AuthUser(permissions.BasePermission):
    """Аутентифицированный пользователь — может, как и Аноним, читать всё,
    дополнительно он может публиковать отзывы и ставить оценку
    произведениям, может комментировать чужие отзывы; может редактировать
    и удалять свои отзывы и комментарии. Эта роль присваивается
    по умолчанию каждому новому пользователю."""
    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user
                or request.method in permissions.SAFE_METHODS)


class Moderator(permissions.BasePermission):
    """Те же права, что и у Аутентифицированного пользователя плюс
    право удалять любые отзывы и комментарии."""
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

    def has_permission(self, request, view):
        return request.method in (['PATCH', 'DELETE']
                                  or permissions.SAFE_METHODS)


class AdminFullAccess(permissions.BasePermission):
    """полные права на управление всем контентом проекта.
    Может создавать и удалять произведения, категории и жанры.
    Может назначать роли пользователям."""
    def has_permission(self, request, view):
        return request.user.role == 'admin' or request.user.is_superuser
