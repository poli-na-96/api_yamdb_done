from django.contrib.auth.models import AbstractUser
from django.core.validators import (RegexValidator,
                                    MaxValueValidator,
                                    MinValueValidator)
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

    username = models.CharField(max_length=150, unique=True,
                                verbose_name='Имя пользователя',
                                validators=[
                                    RegexValidator(
                                        regex='^[a-zA-Z0-9@/./+/-/_]*$',
                                        message='Можно использовать только '
                                        'латинские буквы, цифры и символы '
                                        '@/./+/-/_')
                                ])
    email = models.EmailField(max_length=254, unique=True,
                              verbose_name='Почта')
    first_name = models.CharField(max_length=150, blank=True,
                                  verbose_name='Имя')
    last_name = models.CharField(max_length=150, blank=True,
                                 verbose_name='Фамилия')
    bio = models.TextField(blank=True, verbose_name='Биография')
    role = models.CharField(choices=CHOICES,
                            max_length=15,
                            default=USER,
                            verbose_name='Роль')
    confirmation_code = models.CharField(max_length=20,
                                         verbose_name='Код подтверждения')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Category(models.Model):
    """Категория произведения."""
    name = models.CharField(max_length=256, verbose_name='Название категории')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанр произведения."""
    name = models.CharField(max_length=256, verbose_name='Название жанра')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Слаг')

    class Meta:
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
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Отзывы."""
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews',
                              verbose_name='Произведение')
    text = models.TextField(verbose_name='Текст отзыва')
    score = models.IntegerField(verbose_name='Оценка', validators=(
        MinValueValidator(1), MaxValueValidator(10)
    )
    )
    author = models.ForeignKey(User, verbose_name='Автор отзыва',
                               on_delete=models.CASCADE,
                               related_name='reviews',)
    pub_date = models.DateTimeField(verbose_name='Дата отзыва',
                                    auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Комментарии."""
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Автор комментария')
    pub_date = models.DateTimeField(verbose_name='Дата комментария',
                                    auto_now_add=True,)
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Отзыв')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
