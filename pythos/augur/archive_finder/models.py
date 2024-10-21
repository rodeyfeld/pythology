from django.db import models
from core.models import SensorType, TimestampModel
from provider.models import Collection, Order
from django.contrib.gis.db import models as geomodels
from django.contrib.gis.geos import GEOSGeometry

MINIMUM_BOUNDING_BOX_KM2 = 1

class ArchiveFinder(TimestampModel):

    class Status(models.TextChoices):
        INITIALIZED = "INITIALIZED"
        SEEKING = "SEEKING"
        FINISHED = "FINISHED"
        FAILED = "FAILED"

    name = models.CharField(blank=True, default="", max_length=256)
    geometry = geomodels.GeometryField()
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=128, choices=Status, default=Status.INITIALIZED, blank=True)
    rules = models.CharField(max_length=65536, blank=True, default='') #jsonfield

    @property
    def minimum_polygon_from_point(self) -> GEOSGeometry:
        if self.geometry.geom_type == "Point":
            return self.geometry.buffer(MINIMUM_BOUNDING_BOX_KM2)
        return self.geometry

class ArchiveResult(TimestampModel):

    archive_finder = models.ForeignKey(ArchiveFinder, on_delete=models.CASCADE)
    external_id = models.CharField(blank=True, default='', max_length=2048)
    seeker_run_id = models.CharField(blank=True, default='', max_length=2048)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    sensor_type = models.ForeignKey(SensorType, on_delete=models.CASCADE)
    geometry = geomodels.GeometryField()
    thumbnail=models.CharField(blank=True, default='', max_length=2048)
    metadata = models.CharField(max_length=65536, blank=True, default='') #jsonfield

class ArchiveOrder(TimestampModel):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    archive_result = models.ForeignKey(ArchiveResult, on_delete=models.CASCADE)