from django.db import models
from archive_finder.models import ArchiveItem, ArchiveStudy
from provider.models import Collection
from core.models import Sensor, TimestampModel
from django.contrib.gis.db import models as geomodels

from archive_finder.studies.imagery_lookup.seeker import ImageryLookupSeeker
from archive_finder.studies.imagery_lookup.diviner import ImageryLookupDiviner

class ImageryLookupStudy(ArchiveStudy):
    

    class DreamName(models.TextChoices):
        IMAGERY_FINDER = "IMAGERY_FINDER"

    DREAM_CHART = {
        DreamName.IMAGERY_FINDER: {
            "seeker": ImageryLookupSeeker,
            "diviner": ImageryLookupDiviner,
            "dag_name": "imagery_finder",
        }
    }

    archive_item = models.ForeignKey(ArchiveItem, null=True, on_delete=models.SET_NULL)

class ImageryLookupResult(TimestampModel):

    imagery_lookup_study = models.ForeignKey(ImageryLookupStudy, null=True, on_delete=models.SET_NULL)
    external_id = models.CharField(blank=True, default='', max_length=2048)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    geometry = geomodels.GeometryField()
    thumbnail=models.CharField(blank=True, default='', max_length=2048)
    metadata = models.CharField(max_length=65536, blank=True, default='') #jsonfield

