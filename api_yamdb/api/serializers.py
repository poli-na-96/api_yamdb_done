from django.db.models import Avg
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Genre, Category, Comment, Review, Title
from user.models import User


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации."""
    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError('username me запрещен')
        return data


class TokenSerializer(serializers.Serializer):
    """Сериализатор для токена."""
    username = serializers.SlugField(required=True)
    confirmation_code = serializers.SlugField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для User."""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'bio', 'role', 'email')
        read_only_field = ('role',)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')
    title = serializers.SlugRelatedField(slug_field='id', read_only=True)

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title_id = self.context.get('view').kwargs.get('title_id')
            if Review.objects.filter(
                title=get_object_or_404(Title, pk=title_id),
                author=self.context['request'].user
            ).exists():
                raise serializers.ValidationError('Нельзя оставлять '
                                                  'несколько отзывов')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""
    author = author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')
    review = serializers.SlugRelatedField(slug_field='id', read_only=True)

    class Meta:
        fields = '__all__'
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
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id',
                  'name',
                  'year',
                  'rating',
                  'description',
                  'genre',
                  'category')

    def validate_year(self, value):
        if value > timezone.now().year:
            raise serializers.ValidationError('Год выпуска не может '
                                              'быть больше текущего года.')
        return value

    def get_rating(self, obj):
        avg_score = obj.reviews.aggregate(Avg('score'))['score__avg']
        return avg_score if avg_score is not None else None


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
        required=True
    )

    class Meta:
        model = Title
        fields = '__all__'
