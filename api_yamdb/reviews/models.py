from django.contrib.auth import get_user_model
from django.core.validators import (MaxValueValidator,
                                    MinValueValidator)
from django.db import models

from .validators import validation_year


User = get_user_model()


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


class GenreTitle(models.Model):
    """Модель для связи id произведения и id жанра."""
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'



class Review(models.Model):
    """Отзыв на произведение."""
    text = models.TextField(verbose_name='Отзыв')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='reviews',
                               verbose_name='Автор отзыва')
    score = models.SmallIntegerField(verbose_name='Оценка отзыва',
                                     validators=(MinValueValidator(1),
                                                 MaxValueValidator(10)))
    pub_date = models.DateTimeField('Дата добавления отзыва',
                                    auto_now_add=True)
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='reviews',
                              verbose_name='Произведение')

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review_from_one_author'
            )
        ]

    def __str__(self):
        self.text


class Comment(models.Model):
    """Комментарий к отзыву."""
    text = models.TextField(verbose_name='Комментарий')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Автор комментария')
    pub_date = models.DateTimeField('Дата добавления', auto_now_add=True)
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Отзыв')

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        self.text
