from rest_framework import serializers
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.core.validators import RegexValidator

from reviews.models import Category, Comment, Genre, Review, Title
from user.models import User
from user.validators import validate_username
from user.constants import (MAX_LENGTH_EMAIL, MAX_LENGTH_USERNAME)


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации."""
    email = serializers.EmailField(max_length=MAX_LENGTH_EMAIL)
    username = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME,
        validators=(
            RegexValidator(
                regex='^[a-zA-Z0-9@/./+/-/_]*$',
                message='Можно использовать только '
                'латинские буквы, цифры и символы '
                '@/./+/-/_'
            ), validate_username))

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        try:
            User.objects.get_or_create(
                username=data.get('username'),
                email=data.get('email')
            )
        except Exception:
            raise serializers.ValidationError('поле email или username занято')
        return data


class TokenSerializer(serializers.Serializer):
    """Сериализатор для токена."""

    username = serializers.SlugField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError('Неверный код подтверждения')
        return data


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для User."""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'bio', 'role', 'email')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')
    title = serializers.SlugRelatedField(slug_field='id', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        model = Review

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title_id = self.context.get('view').kwargs.get('title_id')
            if Review.objects.filter(title=title_id,
                                     author=self.context['request'].user
                                     ).exists():
                raise serializers.ValidationError('Нельзя оставлять '
                                                  'несколько отзывов')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')
    review = serializers.SlugRelatedField(slug_field='id', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', 'review', )
        model = Comment


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleGETSerializer(serializers.ModelSerializer):
    """Сериализатор для GET запросов к произведениям."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Title
        fields = ('id',
                  'name',
                  'year',
                  'rating',
                  'description',
                  'genre',
                  'category')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для POST, PUT, DELETE, PATCH запросов к произведениям."""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        required=True
    )
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug',
        required=True,
        allow_empty=False,
        allow_null=False
    )

    class Meta:
        model = Title
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        genre_representation = GenreSerializer(instance.genre, many=True).data
        category_representation = CategorySerializer(instance.category).data

        representation['genre'] = genre_representation
        representation['category'] = category_representation

        return representation
