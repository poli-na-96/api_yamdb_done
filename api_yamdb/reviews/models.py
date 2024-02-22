from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.constants import (MAX_LENGTH_CAT_AND_GENRE_NAME,
                               MAX_LENGTH_CAT_AND_GENRE_SLUG,
                               MAX_LENGTH_TITLE_NAME, MAX_SCORE, MAX_TO_SHOW,
                               MESSAGE, MIN_SCORE)
from reviews.validators import validation_year

User = get_user_model()


class CatOrGenre(models.Model):
    """Абстрактный класс для категорий и жанров."""

    name = models.CharField(max_length=MAX_LENGTH_CAT_AND_GENRE_NAME,
                            verbose_name='Название')
    slug = models.SlugField(unique=True,
                            max_length=MAX_LENGTH_CAT_AND_GENRE_SLUG,
                            verbose_name='Слаг')

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(CatOrGenre):
    """Категория произведения."""

    class Meta(CatOrGenre.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CatOrGenre):
    """Жанр произведения."""

    class Meta(CatOrGenre.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Название произведения."""

    name = models.CharField(max_length=MAX_LENGTH_TITLE_NAME,
                            verbose_name='Название произведения')
    year = models.SmallIntegerField(verbose_name='Год выпуска произведения',
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
        verbose_name='Категория',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Модель для связи id произведения и id жанра."""

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class ReviewOrComment(models.Model):
    """Абстрактный класс для отзывов и комментариев."""

    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор')
    pub_date = models.DateTimeField('Дата публикации',
                                    auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('pub_date',)

    def __str__(self):
        self.text[:MAX_TO_SHOW]


class Review(ReviewOrComment):
    """Отзыв на произведение."""

    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка отзыва',
        validators=(MinValueValidator(MIN_SCORE, message=MESSAGE),
                    MaxValueValidator(MAX_SCORE, message=MESSAGE)))
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              verbose_name='Произведение')

    class Meta(ReviewOrComment.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review_from_one_author'
            )
        ]


class Comment(ReviewOrComment):
    """Комментарий к отзыву."""

    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               verbose_name='Отзыв')

    class Meta(ReviewOrComment.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
