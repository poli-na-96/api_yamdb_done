from django.conf import settings

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


def create_and_send_confirmation_code_by_email(user):
    unique_token = default_token_generator.make_token(user[0])
    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код подтверждения: {unique_token}',
        from_email=settings.ADMIN_EMAIL,
        recipient_list=[user[0].email],
        fail_silently=True,
    )
