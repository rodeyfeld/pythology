
from datetime import datetime
import json
from types import NoneType
from typing import Any, Optional
from ninja import Schema
from geojson_pydantic import Point, Polygon
from archive_finder.models import ArchiveResult

class ArchiveItemSchema(Schema):
    id: int
    external_id: str
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


class DreamStatusResponseSchema(Schema):
    status: str



