from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from user.models import User


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='Указанная почта уже используется')],)

    class Meta:
        model = User
        fields = (
            'email',
            'username',
        )
        validators = (
            UniqueTogetherValidator(
                queryset=User.objects.all(), fields=('username', 'email',),
                message='Указанный username занят'
            ),
        )


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class GetTokenSerializer(serializers.Serializer):
    username = serializers.SlugField(required=True)
    confirmation_code = serializers.SlugField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')