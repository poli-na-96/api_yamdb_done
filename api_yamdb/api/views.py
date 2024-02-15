from uuid import uuid4

from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import ADMIN_EMAIL
from .serializers import SignUpSerializer, TokenSerializer
from user.models import User


@api_view(['POST'])
def signup(request):
    user = User.objects.filter(email=request.data.get('email'),
                               username=request.data.get('username'))
    if user.exists():
        create_and_send_confirmation_code_by_email(user)
        return Response(request.data, status=status.HTTP_200_OK)

    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        user = User.objects.get(username=serializer.data.get('username'))
        create_and_send_confirmation_code_by_email(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def token(request):
    serializer = TokenSerializer(data=request.data)
    user = get_object_or_404(User, username=serializer.data.get('username'))
    if (serializer.is_valid(raise_exception=True)
            and request.confirmation_code == user.confirmation_code):
        return Response(
            {'token': str(AccessToken.for_user(user))},
            status=status.HTTP_200_OK
        )
    return Response(
        'Неправильно указаны данные в запросе.',
        status=status.HTTP_400_BAD_REQUEST
    )


def create_and_send_confirmation_code_by_email(user):
    unique_token = uuid4()
    user.update(confirmation_code=str(unique_token))
    send_mail(
        subject='Код подтверждения',
        message='Ваш код подтверждения: {user.confirmation_code}',
        from_email=ADMIN_EMAIL,
        recipient_list=[user.email],
        fail_silently=True,
    )
