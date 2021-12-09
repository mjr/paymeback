from uuid import uuid4

from django.db import models

from behaviors.behaviors import Timestamped, StoreDeleted
from simple_history.models import HistoricalRecords


class UUIDIdentifier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class BaseModel(UUIDIdentifier, Timestamped, StoreDeleted):
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True
