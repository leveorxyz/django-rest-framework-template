from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField,
    EmailField,
)
from rest_framework.exceptions import ValidationError
from cryptography.fernet import InvalidToken

from core.classes import ExpiringActivationTokenGenerator
from .models import (
    User,
)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email")


class UserLoginSerializer(ModelSerializer):
    username = CharField(source="get_username", read_only=True)

    class Meta:
        model = User
        fields = list(
            set(field.name for field in model._meta.fields) - set(["_profile_photo"])
        ) + ["token", "profile_photo", "username"]
        extra_kwargs = {field: {"read_only": True} for field in fields}
        extra_kwargs["password"] = {"write_only": True}
        del extra_kwargs["email"]


class UserSignUpSerializer(ModelSerializer):
    profile_photo = CharField(required=False)

    def validate(self, attrs):
        if User.objects.filter(email=attrs["email"]).exists():
            raise ValidationError("User with this mail already exists.")
        return super().validate(attrs)

    def create(self, validated_data):
        user = User.from_validated_data(validated_data)

        if validated_data.get("profile_photo"):
            user.profile_photo = validated_data["profile_photo"]

        user.save()

        return user

    class Meta:
        model = User
        fields = list(
            set(field.name for field in model._meta.fields)
            - set(User.get_hidden_fields() + ["_profile_photo", "last_login"])
        ) + ["token", "profile_photo"]
        extra_kwargs = {
            "password": {"write_only": True, "required": True},
            "token": {"read_only": True},
            "email": {"required": True},
        }


class VerifyEmailSerializer(Serializer):
    token = CharField(required=True, write_only=True)

    def validate(self, data):
        try:
            email = ExpiringActivationTokenGenerator().get_token_value(data["token"])
        except InvalidToken:
            raise ValidationError("Invalid token")

        try:
            user = User.objects.get(email=email)
            data["user"] = user
        except User.DoesNotExist:
            raise ValidationError("User does not exist")

        user.is_active = True
        user.is_verified = True
        user.save()

        return data


class PasswordResetEmailSerializer(Serializer):
    email = EmailField(required=True)

    def validate(self, data):
        try:
            user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            raise ValidationError("User does not exist")

        data["user"] = user
        return data


class PasswordResetSerializer(Serializer):
    password = CharField(required=True)
    token = CharField(required=True)
