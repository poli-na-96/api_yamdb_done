from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from .validators import validation_year

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

CHOICES = (
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
)


class User(AbstractUser):
    """Кастомная модель пользователя."""
    pass


class Category(models.Model):
    """Категория произведения."""
    name = models.CharField(max_length=256, verbose_name='Название категории')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Слаг')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанр произведения."""
    name = models.CharField(max_length=256, verbose_name='Название жанра')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Слаг')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Название произведения."""
    name = models.CharField(max_length=256,
                            verbose_name='Название произведения')
    year = models.IntegerField(verbose_name='Год выпуска произведения',
                               validators=[validation_year])
    description = models.TextField(null=True, blank=True,
                                   verbose_name='Описание произведения')
    genre = models.ManyToManyField(
        Genre, verbose_name='Жанр', related_name='titles',
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Отзывы."""
    pass


class Comment(models.Model):
    """Комментарии."""
    pass
