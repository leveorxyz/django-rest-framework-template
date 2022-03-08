from django.contrib import admin

from .models import (
    User,
)

# Register your models here.
models = [
    User,
]
for model in models:
    admin.site.register(model)
