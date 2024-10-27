from django.contrib import admin
from augury.models import ArchiveItem
from core.admin import TimeStampAdminMixin


@admin.register(ArchiveItem)
class ArchiveItemAdmin(admin.ModelAdmin, TimeStampAdminMixin):
    list_display = [
        "external_id",
        "collection",
        "provider",
        "start_date",
        "end_date",
        "sensor_type",
        "thumbnail",
        "geometry",
     ] + TimeStampAdminMixin.list_display
