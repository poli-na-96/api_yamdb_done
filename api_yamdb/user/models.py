from django.db import models

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


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