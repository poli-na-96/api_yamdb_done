from django.contrib.auth import get_user_model
from django.core.validators import (MaxValueValidator,
                                    MinValueValidator)
from django.db import models

User = get_user_model()


class Title(models.Model):
    pass


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
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        self.text
