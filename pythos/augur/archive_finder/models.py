from django.db import models
from archive_finder.studies.imagery_lookup.seeker import ImageryLookupSeeker
from archive_finder.studies.imagery_lookup.diviner import ImageryLookupDiviner
from augury.mystics.seeker import Seeker
from augury.mystics.diviner import Diviner
from core.models import TimestampModel
from django.contrib.gis.db import models as geomodels
from django.contrib.gis.geos import GEOSGeometry

MINIMUM_BOUNDING_BOX_KM2 = 1

class ArchiveFinder(TimestampModel):

    name = models.CharField(blank=True, default="", max_length=256)
    geometry = geomodels.GeometryField()
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    rules = models.CharField(max_length=65536, blank=True, default='') #jsonfield

    @property
    def minimum_polygon_from_point(self) -> GEOSGeometry:
        if self.geometry.geom_type == "Point":
            return self.geometry.buffer(MINIMUM_BOUNDING_BOX_KM2)
        return self.geometry

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

class Study(TimestampModel):
    
    class Status(models.TextChoices):
        INITIALIZED = "INITIALIZED"
        RUNNING = "RUNNING"
        SUCCESS = "SUCCESS"
        FAILED = "FAILED"
        ANOMALOUS = "ANOMALOUS"

    class DreamName(models.TextChoices):
        IMAGERY_FINDER = "IMAGERY_FINDER"
        
    DREAM_CHART = {
        DreamName.IMAGERY_FINDER: {
            "seeker": ImageryLookupSeeker,
            "diviner": ImageryLookupDiviner,
            "dag_name": "imagery_finder",
        }
    }
    
    archive_finder = models.ForeignKey(ArchiveFinder, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, choices=DreamName, default=DreamName.IMAGERY_FINDER, blank=True)
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