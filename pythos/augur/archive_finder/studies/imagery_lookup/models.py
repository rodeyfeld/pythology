from django.db import models
from archive_finder.models import ArchiveFinder, ArchiveItem
from augury.models import Study
from provider.models import Collection
from core.models import Sensor, TimestampModel
from django.contrib.gis.db import models as geomodels

class ImageryLookupStudy(Study):

    archive_item = models.ForeignKey(ArchiveItem, null=True, on_delete=models.SET_NULL)
    archive_finder = models.ForeignKey(ArchiveFinder, on_delete=models.CASCADE)

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

