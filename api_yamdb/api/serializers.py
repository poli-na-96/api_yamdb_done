from rest_framework import serializers

from user.models import User

from reviews.models import Comment, Review, Title
from django.db.models import Avg
from django.utils import timezone
from rest_framework import serializers, validators

from reviews.models import (Title, Genre, Category)


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError('username me запрещен')
        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.SlugField(required=True)
    confirmation_code = serializers.SlugField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'bio', 'role', 'email')
        read_only_field = ('role',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')
    title = serializers.SlugRelatedField(slug_field='id', read_only=True)

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        if Review.objects.filter(author=self.context['request'].user).exists():
            raise serializers.ValidationError('Нельзя оставлять несколько отзывов')
        return data


class CommentSerializer(serializers.ModelSerializer):
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
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""
    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleGETSerializer(serializers.ModelSerializer):
    """Сериализатор для GET запросов к произведениям."""
    category = CategorySerializer(read_only=True, many=True)
    genre = GenreSerializer(read_only=True)
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
        return avg_score if avg_score is not None else 0


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
