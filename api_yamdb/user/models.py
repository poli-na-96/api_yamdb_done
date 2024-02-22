from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from user.constants import (CHOICES, MAX_LENGTH_EMAIL, MAX_LENGTH_USERNAME,
                            MODERATOR, ADMIN, USER)
from user.utils import max_length_role
from user.validators import validate_username


class User(AbstractUser):
    """Кастомная модель пользователя."""

    username = models.CharField(max_length=MAX_LENGTH_USERNAME,
                                unique=True,
                                verbose_name='Имя пользователя',
                                validators=[
                                    RegexValidator(
                                        regex='^[a-zA-Z0-9@/./+/-/_]*$',
                                        message='Можно использовать только '
                                        'латинские буквы, цифры и символы '
                                        '@/./+/-/_'
                                    ),
                                    validate_username
                                ])
    email = models.EmailField(max_length=MAX_LENGTH_EMAIL, unique=True,
                              verbose_name='Почта')
    bio = models.TextField(blank=True, verbose_name='Биография')
    role = models.CharField(choices=CHOICES,
                            max_length=max_length_role(),
                            default=USER,
                            verbose_name='Роль')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    @property
    def is_admin(self):
        return (self.role == ADMIN or self.is_superuser
                or self.is_staff)

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    def __str__(self):
        return self.username
