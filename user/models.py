from __future__ import annotations

from django.db import models, IntegrityError
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.models import Site
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from core.classes import ExpiringActivationTokenGenerator
from core.models import CoreModel
from core.literals import (
    PROFILE_PHOTO_DIRECTORY,
)
from core.modelutils import send_mail
from .utils import generate_file_and_name

# Create your models here.

username_validator = UnicodeUsernameValidator()


class PasswordResetWhitelist(CoreModel):
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=255, unique=True)


class User(AbstractUser, CoreModel):
    class UserType(models.TextChoices):
        ADMIN = "ADMIN", _("admin")
        NORMAL = "NORMAL", _("normal")

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_("Required. 150 characters or fewer. Letters and digits only."),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    first_name = None
    last_name = None
    full_name = models.CharField(_("full name"), max_length=180, blank=True)
    email = models.EmailField(_("email"), unique=True)
    user_type = models.CharField(
        _("user type"),
        max_length=20,
        choices=UserType.choices,
        default=UserType.NORMAL,
        blank=True,
    )
    is_verified = models.BooleanField(
        _("is verified"), default=False, blank=True, null=True
    )
    street = models.CharField(_("street"), max_length=100, blank=True, null=True)
    state = models.CharField(_("state"), max_length=50, blank=True, null=True)
    city = models.CharField(_("city"), max_length=50, blank=True, null=True)
    zip_code = models.CharField(_("zip code"), max_length=15, blank=True, null=True)
    contact_no = models.CharField(_("contact no"), max_length=20, blank=True, null=True)
    _profile_photo = models.ImageField(
        upload_to=PROFILE_PHOTO_DIRECTORY,
        blank=True,
        null=True,
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    @classmethod
    def from_validated_data(cls, validated_data: dict):
        fields = [field.name for field in User._meta.fields]

        validated_data["password"] = make_password(validated_data.pop("password"))
        constructor_kwargs = {
            field: validated_data.pop(field)
            for field in fields
            if field in validated_data
        }
        return cls(**constructor_kwargs)

    @classmethod
    def get_hidden_fields(self) -> list:
        return super().get_hidden_fields() + [
            "is_staff",
            "is_superuser",
            "is_verified",
            "_profile_photo",
            "is_active",
            "date_joined",
        ]

    @property
    def token(self) -> str:
        try:
            token, _ = Token.objects.get_or_create(user=self)
            return token.key
        except Token.DoesNotExist:
            raise AuthenticationFailed("Token expired.")

    @property
    def profile_photo(self) -> str:
        domain = Site.objects.get_current().domain
        if self._profile_photo.name:
            return domain + self._profile_photo.url

    @profile_photo.setter
    def profile_photo(self, profile_photo_data):
        if self._profile_photo.name:
            del self.profile_photo
        file_name, file = generate_file_and_name(profile_photo_data, self.id)
        self._profile_photo.save(file_name, file, save=True)
        self.save()

    @profile_photo.deleter
    def profile_photo(self):
        if self._profile_photo.name:
            self._profile_photo.delete(save=True)

    def delete(self, *args, **kwargs):
        del self.profile_photo
        return super(User, self).delete(*args, **kwargs)

    def send_email_verification_mail(self):
        template = "email/account_verification.html"

        confirmation_token = ExpiringActivationTokenGenerator().generate_token(
            text=self.email
        )

        link = (
            "/".join(
                [
                    settings.FRONTEND_URL,
                    "email-verification",
                ]
            )
            + f"?token={confirmation_token.decode('utf-8')}"
        )
        send_mail(
            to_email=self.email,
            subject=f"Welcome, please verify your email address",
            template_name=template,
            input_context={
                "name": self.full_name,
                "link": link,
                "host_url": Site.objects.get_current().domain,
            },
        )

    def send_password_reset_mail(self):

        template = "email/password_reset.html"

        reset_token = ExpiringActivationTokenGenerator().generate_token(text=self.email)

        try:
            _ = PasswordResetWhitelist.objects.create(
                email=self.email, token=reset_token.decode("utf-8")
            )
        except IntegrityError:
            raise ValidationError("Password reset mail is already sent.")

        link = (
            "/".join(
                [
                    settings.FRONTEND_URL,
                    "password-reset",
                ]
            )
            + f"?token={reset_token.decode('utf-8')}"
        )
        send_mail(
            to_email=self.email,
            subject=f"Password Reset",
            template_name=template,
            input_context={
                "name": self.full_name,
                "link": link,
                "host_url": Site.objects.get_current().domain,
            },
        )

    @classmethod
    def verify_password_reset(cls, token: str, password: str) -> None:
        user = None
        whitelist_token = None
        try:
            whitelist_token = PasswordResetWhitelist.objects.get(token=token)
        except PasswordResetWhitelist.DoesNotExist:
            raise ValidationError("Invalid token.")
        email = ExpiringActivationTokenGenerator().get_token_value(token)

        try:
            user = cls.objects.get(email=email)
        except cls.DoesNotExist:
            raise ValidationError("Invalid token.")

        user.set_password(password)
        user.save()
        whitelist_token.delete()

    def get_username(self) -> str:
        return self.username

    def __str__(self) -> str:
        return self.email

    def __repr__(self) -> str:
        return self.email


class UserIp(CoreModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f"{self.user.id}-{self.ip_address}"
