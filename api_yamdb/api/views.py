from uuid import uuid4

from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import ADMIN_EMAIL
from .serializers import SignUpSerializer, TokenSerializer
from user.models import User

from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404
# from django.shortcuts import render
from .serializers import CommentSerializer, ReviewSerializer
from reviews.models import Review, Title

# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Title, Genre, Category
from .serializers import (TitleGETSerializer, TitleSerializer,
                          GenreSerializer, CategorySerializer)
# from .permissions import AdminOrReadOnly


@api_view(['POST'])
def signup(request):
    user = User.objects.filter(email=request.data.get('email'),
                               username=request.data.get('username'))
    if user.exists():
        create_and_send_confirmation_code_by_email(user)
        return Response(request.data, status=status.HTTP_200_OK)

    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        user = User.objects.get(username=serializer.data.get('username'))
        create_and_send_confirmation_code_by_email(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def token(request):
    serializer = TokenSerializer(data=request.data)
    user = get_object_or_404(User, username=serializer.data.get('username'))
    if (serializer.is_valid(raise_exception=True)
            and request.confirmation_code == user.confirmation_code):
        return Response(
            {'token': str(AccessToken.for_user(user))},
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
        recipient_list=[user.email],
        fail_silently=True,
    )


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)

        
class GenreViewSet(viewsets.ModelViewSet):
    """Получение, добавление, удаление жанра."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = [AdminOrReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(viewsets.ModelViewSet):
    """Получение, добавление, удаление категории."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [AdminOrReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Получение, добавление, изменение и удаление произведения."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # permission_classes = [AdminOrReadOnly]
    pagination_class = LimitOffsetPagination
    # filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')

    def get_serializer_class(self):
        """Определяет какой сериализатор будет использоваться
        для разных типов запроса."""
        if self.request.method == 'GET':
            return TitleGETSerializer
        return TitleSerializer