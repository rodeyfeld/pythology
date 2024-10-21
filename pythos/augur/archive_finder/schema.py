
from datetime import datetime
import json
from types import NoneType
from typing import Any, Optional
from ninja import Schema
from geojson_pydantic import Point, Polygon
from archive_finder.models import ArchiveResult

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

    
class ArchiveResultSchema(Schema):
    id: int
    archive_finder_id: int
    external_id: str
    seeker_run_id: str
    collection: str
    start_date: datetime
    end_date: datetime
    sensor_type: str
    geometry: Polygon
    thumbnail: str


    @staticmethod
    def resolve_geometry(obj: ArchiveResult):
        geojson = json.loads(obj.geometry.geojson)
        return geojson

    @staticmethod
    def resolve_collection(obj: ArchiveResult):
        return obj.collection.name
    
        
    @staticmethod
    def resolve_sensor_type(obj: ArchiveResult):
        return obj.sensor_type.technique
        
    
    @staticmethod
    def resolve_archive_finder_id(obj: ArchiveResult):
        return obj.pk        
    

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

class ArchiveFinderSeekerRequestSchema(Schema):
    archive_finder_id: int

class ArchiveFinderSeekerStatusResponseSchema(Schema):
    status: str


class ArchiveFinderSeekerAudienceRequestSchema(Schema):
    archive_finder_id: int
    start_date: datetime 
    end_date: datetime 
    sortby: str


class ArchiveResultSeekerAudienceResponseSchema(Schema):
    id: str
    archive_finder_id: int
    catalogs: list[dict[str, Any]] #TODO Formalize this schema



