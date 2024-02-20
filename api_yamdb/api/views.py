from uuid import uuid4

from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import ADMIN_EMAIL
from reviews.models import Category, Genre, Review, Title
from user.models import User

from .filters import TitleFilterSet
from .mixins import GetListCreateDeleteMixin
from .permissions import (ReviewOrCommentPermission, SuperUserOrAdminOnly,
                          TitlePermission)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, SignUpSerializer,
                          TitleGETSerializer, TitleSerializer, TokenSerializer,
                          UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели User."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (SuperUserOrAdminOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(methods=['get', 'patch'], detail=False, url_path='me',
            url_name='me', permission_classes=(IsAuthenticated,))
    def get_me_patch(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(request.user,
                                        data=request.data,
                                        partial=True,
                                        context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Регистрация пользователя."""

    user = User.objects.filter(email=request.data.get('email'),
                               username=request.data.get('username'))
    if user.exists():
        create_and_send_confirmation_code_by_email(user)
        return Response(request.data, status=status.HTTP_200_OK)

    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = User.objects.filter(email=serializer.data.get('email'),
                               username=serializer.data.get('username'))
    create_and_send_confirmation_code_by_email(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    """Получение JWT токена."""

    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = get_object_or_404(User, username=serializer.data.get(
            'username'))
        if request.data.get('confirmation_code') == user.confirmation_code:
            return Response(
                {'token': str(AccessToken.for_user(get_object_or_404(
                    User, username=serializer.data.get('username'))))},
                status=status.HTTP_200_OK
            )
    return Response(
        'Неправильно указаны данные в запросе.',
        status=status.HTTP_400_BAD_REQUEST
    )


def create_and_send_confirmation_code_by_email(user):
    unique_token = uuid4()
    user.update(confirmation_code=str(unique_token))
    send_mail(
        subject='Код подтверждения',
        message='Ваш код подтверждения: {user.confirmation_code}',
        from_email=ADMIN_EMAIL,
        recipient_list=[user[0].email],
        fail_silently=True,
    )


class ReviewsViewSet(viewsets.ModelViewSet):
    """Получение, создание, удаление, редактирование отзыва."""

    serializer_class = ReviewSerializer
    permission_classes = (ReviewOrCommentPermission,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    """Получение, создание, удаление, редактирование комментария."""

    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (ReviewOrCommentPermission,)

    def get_review(self):
        return get_object_or_404(Review, title_id=self.kwargs.get('title_id'),
                                 id=self.kwargs.get('review_id'))

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)


class GenreViewSet(GetListCreateDeleteMixin):
    """Получение, добавление, удаление жанра."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(GetListCreateDeleteMixin):
    """Получение, добавление, удаление категории."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Получение, добавление, изменение и удаление произведения."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [TitlePermission]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = TitleFilterSet
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    ordering_fields = ['name', 'genre', 'category']

    def get_serializer_class(self):
        """Определяет какой сериализатор будет использоваться
        для разных типов запроса."""

        if self.request.method in permissions.SAFE_METHODS:
            return TitleGETSerializer
        return TitleSerializer
