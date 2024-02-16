from rest_framework import permissions


class AnonimReadOnly(permissions.BasePermission):
    """может просматривать описания произведений,
    читать отзывы и комментарии."""
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class AuthUserOrReadOnly(permissions.BasePermission):
    """Аутентифицированный пользователь — может, как и Аноним, читать всё,
    дополнительно он может публиковать отзывы и ставить оценку
    произведениям, может комментировать чужие отзывы; может редактировать
    и удалять свои отзывы и комментарии. Эта роль присваивается
    по умолчанию каждому новому пользователю."""
    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user
                or request.method in permissions.SAFE_METHODS)

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class Moderator(permissions.BasePermission):
    """Те же права, что и у Аутентифицированного пользователя плюс
    право удалять любые отзывы и комментарии."""
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.user.role == 'moder'

    def has_permission(self, request, view):
        return request.user.role == 'moder'


class SuperUserOrAdminOnly(permissions.BasePermission):
    """полные права на управление всем контентом проекта.
    Может создавать и удалять произведения, категории и жанры.
    Может назначать роли пользователям."""
    def has_permission(self, request, view):
        return ((request.user.role == 'admin'
                or request.user.is_superuser or request.user.is_staff)
                and request.user.is_authenticated)


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and (request.user.role == 'admin'
                or request.user.is_superuser
                or request.user.is_staff))
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return False
        return True


class TitlePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user.is_authenticated and request.user.role == 'admin'

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return request.user.is_authenticated and (
            request.user.is_superuser
            or request.user.is_staff
            or request.user.role == 'admin'
        )


class SuperUserOrAdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and (
                request.user.is_superuser
                or request.user.role == 'admin'
                or request.user.is_staff
            )
        )


class ReviewOrCommentPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and (
                request.user.is_superuser
                or request.user.is_staff
                or request.user.role == 'admin'
                or request.user.role == 'moderator'
                or request.user == obj.author))
