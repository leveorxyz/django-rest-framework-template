import os
from typing import Optional
from cryptography.fernet import Fernet, InvalidToken
from datetime import datetime, timedelta, timezone

from django.core.files.storage import FileSystemStorage
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed, ValidationError


class OverwriteFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name: str, max_length: Optional[int]):
        if self.exists(name):
            self.delete(name)
        return name


class FileManager:
    def __init__(self):
        self.storage_system = OverwriteFileSystemStorage()

    def save_file(self, file: any, *folder_path):
        file_path = os.path.join(settings.MEDIA_ROOT, *folder_path, file.name)
        self.storage_system.save(file_path, file)
        return file_path

    def delete_file(self, path: str):
        self.storage_system.delete(path)


class CustomTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"

    def expires_in(self, token):
        time_elapsed = datetime.now(timezone.utc) - token.created
        return (
            timedelta(seconds=settings.USER_AUTH_TOKEN_EXPIRATION_SECONDS)
            - time_elapsed
        )

    def is_expired(self, token):
        return self.expires_in(token) < timedelta(seconds=0)

    def authenticate_credentials(self, key):
        try:
            token = self.get_model().objects.get(key=key)
        except self.get_model().DoesNotExist:
            raise AuthenticationFailed("Invalid token.")

        if not token.user.is_active:
            raise AuthenticationFailed("User inactive or deleted.")

        if self.is_expired(token):
            token.delete()
            raise AuthenticationFailed("Token expired.")

        return (token.user, token)


class ExpiringActivationTokenGenerator:
    FERNET_KEY = settings.FERNET_KEY
    fernet = Fernet(FERNET_KEY)

    DATE_FORMAT = "%Y-%m-%d %H-%M-%S"
    EXPIRATION_DAYS = 3

    def _get_time(self):
        """Returns a string with the current UTC time"""
        return datetime.utcnow().strftime(self.DATE_FORMAT)

    def _parse_time(self, d):
        """Parses a string produced by _get_time and returns a datetime object"""
        return datetime.strptime(d, self.DATE_FORMAT)

    def generate_token(self, text):
        """Generates an encrypted token"""
        full_text = text + "|" + self._get_time()
        token = self.fernet.encrypt(bytes(full_text, encoding="utf-8"))
        return token

    def get_token_value(self, token):
        """Gets a value from an encrypted token.
        Returns None if the token is invalid or has expired.
        """
        try:
            value = self.fernet.decrypt(bytes(token, encoding="utf-8")).decode("utf-8")
            separator_pos = value.rfind("|")

            text = value[:separator_pos]
            token_time = self._parse_time(value[separator_pos + 1 :])

            if token_time + timedelta(self.EXPIRATION_DAYS) < datetime.utcnow():
                raise InvalidToken("Token expired.")
        except InvalidToken:
            raise ValidationError("Invalid token.")

        return text
