from django.core.exceptions import ValidationError
from django.utils import timezone


def validation_year(value):
    if value > timezone.now().year:
        raise ValidationError('Год выпуска не может быть больше текущего.')
    if value < 0:
        raise ValidationError('Год выпуска не может быть отрицательным.')
