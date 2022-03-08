from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        PASSWORD = "admin"
        EMAIL = "admin@mail.com"

        User = get_user_model()
        if not User.objects.filter(email=EMAIL).exists():
            User.objects.create(
                username="admin",
                email=EMAIL,
                password=make_password(PASSWORD),
                is_staff=True,
                is_superuser=True,
                user_type=User.UserType.ADMIN,
            )
            self.stdout.write(self.style.SUCCESS("Admin user has been created"))
        else:
            self.stdout.write(self.style.ERROR("Admin user already exists"))
