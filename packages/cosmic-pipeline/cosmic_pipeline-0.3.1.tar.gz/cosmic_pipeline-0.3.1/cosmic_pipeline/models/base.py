import uuid

from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(uuid.uuid4,primary_key=True, default=uuid.uuid4, editable=False,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at", "-updated_at"]
        app_label = "cosmic_pipeline"
