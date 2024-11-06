from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from core.models import TimestampModel
from augury.mystics.seeker import Seeker
from augury.mystics.diviner import Diviner

class Dream(TimestampModel):

    class Meta:
        indexes = [
            models.Index(fields=["study_type", "study_id"]),
        ]
    class Status(models.TextChoices):
        INITIALIZED = "INITIALIZED"
        QUEUED = "QUEUED"
        RUNNING = "RUNNING"
        SUCCESS = "SUCCESS"
        PROCESSING = "PROCESSING"
        COMPLETE = "COMPLETE"
        FAILED = "FAILED"
        ANOMALOUS = "ANOMALOUS"

    DREAMFLOW_STATUS_MAP = {
        "queued": Status.QUEUED,
        "running": Status.RUNNING,
        "success": Status.SUCCESS,
        "failed": Status.FAILED,
    }

    study_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    study_id = models.PositiveIntegerField()
    study = GenericForeignKey("study_type", "study_id")
    status = models.CharField(max_length=128, choices=Status, default=Status.INITIALIZED, blank=True)

class Study(TimestampModel):
    
    class Meta:
        abstract = True

    class Status(models.TextChoices):
        INITIALIZED = "INITIALIZED"
        RUNNING = "RUNNING"
        SUCCESS = "SUCCESS"
        FAILED = "FAILED"
        ANOMALOUS = "ANOMALOUS"


    DREAM_CHART = {}
    
    name = models.CharField(max_length=128, blank=True)
    status = models.CharField(max_length=128, choices=Status, default=Status.INITIALIZED, blank=True)

    @property
    def seeker(self) -> Seeker:
        return Study.DREAM_CHART[self.name]["seeker"]()

    @property
    def diviner(self) -> Diviner:
        return Study.DREAM_CHART[self.name]["diviner"]()
    
    @property
    def dag_name(self) -> str:
        return Study.DREAM_CHART[self.name]["dag_name"]