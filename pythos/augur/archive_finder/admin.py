from django.contrib import admin

from core.admin import TimeStampAdminMixin
from archive_finder.models import ArchiveFinder, ArchiveOrder, ArchiveResult


@admin.register(ArchiveFinder)
class ArchiveFinderAdmin(admin.ModelAdmin, TimeStampAdminMixin):
    list_display = [
        "geometry",
        "start_date",
        "end_date",
        "is_active",
     ] + TimeStampAdminMixin.list_display


@admin.register(ArchiveResult)
class ArchiveResultAdmin(admin.ModelAdmin, TimeStampAdminMixin):
    list_display = [
        "archive_finder",
        "external_id",
        "seeker_run_id",
        "collection",
        "start_date",
        "end_date",
        "sensor_type",
        "geometry",
        "metadata",
     ] + TimeStampAdminMixin.list_display


@admin.register(ArchiveOrder)
class ArchiveOrderAdmin(admin.ModelAdmin, TimeStampAdminMixin):
    list_display = [
        "order",
        "archive_result",
     ] + TimeStampAdminMixin.list_display
