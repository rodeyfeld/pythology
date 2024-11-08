
from datetime import datetime
import json
from types import NoneType
from typing import Any, Optional
from ninja import Schema
from geojson_pydantic import Point, Polygon

class ArchiveFinderSchema(Schema):
    id: int 
    name: str 
    start_date: datetime
    end_date: datetime
    is_active: bool
    status: str
    rules: str
    geometry: Point | Polygon

    @staticmethod
    def resolve_geometry(obj):
        geojson = json.loads(obj.geometry.geojson)
        return geojson

class ArchiveFinderRules(Schema):
    is_resolution_max_cm: Optional[int|NoneType] = None
    ais_resolution_min_cm: Optional[int|NoneType] = None
    eo_resolution_max_cm: Optional[int|NoneType] = None
    eo_resolution_min_cm: Optional[int|NoneType] = None
    hsi_resolution_max_cm: Optional[int|NoneType] = None
    hsi_resolution_min_cm: Optional[int|NoneType] = None
    rf_resolution_max_cm: Optional[int|NoneType] = None
    rf_resolution_min_cm: Optional[int|NoneType] = None
    sar_resolution_max_cm: Optional[int|NoneType] = None
    sar_resolution_min_cm: Optional[int|NoneType] = None
    cloud_coverage_pct: Optional[int|NoneType] = None

class ArchiveFinderMetaData(Schema):
    constellation: Optional[str]

class ArchiveFinderCreateRequestSchema(Schema):
    start_date: datetime
    end_date: datetime
    geometry: str
    name: str
    rules: Optional[ArchiveFinderRules] = None

class ArchiveFinderCreateResponseSchema(Schema):
    archive_finder_id: int
    name: str
    start_date: datetime
    end_date: datetime
    geometry: Point | Polygon

class StudyExecuteRequestSchema(Schema):
    archive_finder_id: int
    name: str
