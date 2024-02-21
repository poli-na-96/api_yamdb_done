from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from .validators import validate_username

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
                                        '@/./+/-/_'), validate_username
                                ])
    email = models.EmailField(max_length=254, unique=True,
                              verbose_name='Почта')
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
        ordering = ["username"]

    def is_admin(self, request):
        return request.user.role == 'admin'

    def is_moderator(self, request):
        return request.user.role == 'moderator'

    def __str__(self):
        return self.username


class StreamData:
    def create(self, fields, lst_values):
        if len(fields) != len(lst_values):
            return False
        for i, key in enumerate(fields):
            setattr(self, key, lst_values(i))
        return True
