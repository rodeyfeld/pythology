from django.contrib import admin

from core.admin import TimeStampAdminMixin
from archive_finder.models import ArchiveFinder, ArchiveItem


@admin.register(ArchiveFinder)
class ArchiveFinderAdmin(admin.ModelAdmin, TimeStampAdminMixin):
    list_display = [
        "geometry",
        "start_date",
        "end_date",
        "is_active",
     ] + TimeStampAdminMixin.list_display

@admin.register(ArchiveItem)
class ArchiveItemAdmin(admin.ModelAdmin, TimeStampAdminMixin):
    list_display = [
        "external_id",
        "collection",
        "provider",
        "start_date",
        "end_date",
        "sensor",
        "thumbnail",
        "geometry",
     ] + TimeStampAdminMixin.list_display
