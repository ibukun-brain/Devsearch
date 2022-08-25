import auto_prefetch
from django.db import models
import uuid


class TimeIDBasedModel(auto_prefetch.Model):
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


    class Meta(auto_prefetch.Model.Meta):
        abstract = True