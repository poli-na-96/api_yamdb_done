from rest_framework import serializers

from reviews.models import Comment, Review, Title
from django.db.models import Avg
from django.utils import timezone
from rest_framework import serializers

from reviews.models import (Title, Genre, Category)

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())
    title = serializers.SlugRelatedField(slug_field='id', read_only=True)

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())
    comment = serializers.SlugRelatedField(slug_field='id', read_only=True)

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
