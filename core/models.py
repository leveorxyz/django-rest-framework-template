import uuid
from django.db import models, transaction

# Create your models here.
class CoreModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    @classmethod
    def get_hidden_fields(cls):
        return ["created_at", "updated_at", "is_deleted", "deleted_at"]

    @classmethod
    def from_validated_data(cls, validated_data: dict, *args, **kwargs):
        fields = [field.name for field in cls._meta.fields]

        constructor_kwargs = {
            field: validated_data.pop(field)
            for field in fields
            if field in validated_data
        }
        return cls(**constructor_kwargs)

    def update_from_validated_data(self, validated_data: dict, *args, **kwargs):
        fields = [field.name for field in self._meta.fields]

        for field in fields:
            if field in validated_data:
                setattr(self, field, validated_data.pop(field))

        self.save()

    def __str__(self) -> str:
        return str(self.id)

    def __repr__(self) -> str:
        return self.__str__()

    class Meta:
        abstract = True
