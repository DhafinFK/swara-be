from django.db import models
from uuid6 import uuid7


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDBaseModel(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid7)

    class Meta(BaseModel.Meta):
        abstract = True