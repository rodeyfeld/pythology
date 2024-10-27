from django.db import models
from django.contrib.gis.db import models as geomodels
from core.models import TimestampModel

class ArchiveItem(TimestampModel):
    external_id = models.CharField(blank=True, default='', max_length=2048)
    collection = models.CharField(blank=True, default='', max_length=256)
    provider = models.CharField(blank=True, default='', max_length=256)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    sensor_type = models.CharField(blank=True, default='', max_length=256)
    thumbnail = models.CharField(blank=True, default='', max_length=2048)
    metadata = models.CharField(blank=True, default='', max_length=4096)
    geometry = geomodels.GeometryField()




