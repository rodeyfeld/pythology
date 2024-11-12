from ninja import ModelSchema

from geojson_pydantic import LineString, Point, Polygon
import json
from archive_finder.studies.imagery_lookup.models import ImageryLookupItem, ImageryLookupResult, ImageryLookupStudy


class ImageryLookupStudySchema(ModelSchema):

    study_name: str = ""
    status: str = "ANOMALOUS"
    
    class Meta:
        model = ImageryLookupStudy
        fields = "__all__"

    @staticmethod
    def resolve_study_name(obj):
        return obj.dag_id
    
    
    @staticmethod
    def resolve_status(obj):
        return obj.status

class ImageryLookupItemSchema(ModelSchema):


    class Meta:
        model = ImageryLookupItem
        fields = "__all__"


class ImageryLookupResultSchema(ModelSchema):

    geometry: Point | Polygon | LineString = None
    
    
    class Meta:
        model = ImageryLookupResult
        fields = [
            "study",
            "external_id",
            "collection",
            "start_date",
            "end_date",
            "sensor",
            "thumbnail",
            "metadata",
        ]

    @staticmethod
    def resolve_geometry(obj):
        geojson = json.loads(obj.geometry.geojson)
        return geojson
