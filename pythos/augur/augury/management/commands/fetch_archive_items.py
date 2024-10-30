from datetime import datetime, timedelta
from datetime import timezone
import json
from django.core.management.base import BaseCommand
import pymongo
import requests
from core.models import IntegrationConfigOption, InternalIntegration, SensorType
from archive_finder.utils import geojson_to_geosgeom, is_valid_geometry_type
from augury.models import ArchiveItem
from augury.schema import AudienceRequestSchema, AudienceResponseSchema
from provider.models import Collection, Provider


INTERNAL_INTEGRATION_NAME = 'oracle'


@staticmethod
def format_date(date) -> str:
    return date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

def is_valid_geojson_result(geojson):
    if not is_valid_geometry_type(geojson):
        return False
    return True

def map_sensor_to_technique(sensor: str):
    if sensor in ('EO', 'MSI'):
        return SensorType.TechniqueChoices.EO
    elif sensor in ('SAR'):
        return SensorType.TechniqueChoices.SAR
    return SensorType.TechniqueChoices.UNKNOWN


def create_archive_items(audience_results: AudienceResponseSchema):
    for catalog in audience_results.catalogs:
        catalog_name = catalog['name']
        provider, _ = Provider.objects.get_or_create(
            name=catalog_name
        )
        for catalog_collection in catalog['collections']:
            collection_name = catalog_collection['name']
            collection, _ = Collection.objects.get_or_create(
                name=collection_name,
                provider=provider
            )
            features = catalog_collection['features'] if catalog_collection['features'] else []
            for feature in features:
                geometry_geojson = feature['geometry']
                if is_valid_geojson_result(geometry_geojson):
                    geometry = geojson_to_geosgeom(geometry_geojson)

                    sensor_type_str = feature['sensor_type']
                    technique = map_sensor_to_technique(sensor_type_str)
                    sensor_type, _ = SensorType.objects.get_or_create(
                        technique=technique
                    )
                    archive_item = ArchiveItem.objects.create(
                        external_id=feature['id'],
                        geometry=geometry,
                        collection=collection,
                        sensor_type=sensor_type,
                        thumbnail=feature['assets']['thumbnail']["href"],
                        start_date=feature['start_date'],
                        end_date=feature['end_date'],
                        metadata=str(feature['properties']),
                    )


# JSON File Alternative
def ingest_archive_items(filepath): 
    with open(filepath, 'r') as file:
        data = json.load(file)
        audience_results = AudienceResponseSchema(
            id=data['id'],
            catalogs=data['catalogs']
        )
        create_archive_items(audience_results=audience_results)

# Via Oracle API
def fetch_archive_items(start_date, end_date): 

    internal_integration = InternalIntegration.objects.get(name=INTERNAL_INTEGRATION_NAME)
    payload = AudienceRequestSchema(
        start_date=f"{format_date(start_date)}", 
        end_date=f"{format_date(end_date)}", 
        sortby="datetime",
    )
    payload_json = payload.model_dump_json()        
    internal_stac_endpoint_config = internal_integration.config_options.all().get(key=IntegrationConfigOption.ConfigFieldChoices.STAC_ENDPOINT)
    url = internal_stac_endpoint_config.value
    response = requests.post(url=url, json=payload_json)
    response_data = response.json()
    audience_results = AudienceResponseSchema(
        id=response_data['id'],
        catalogs=response_data['catalogs']
    )
    create_archive_items(audience_results=audience_results)


# Via pymongo
def fetch_from_mongo():

    myclient = pymongo.MongoClient("mongodb://root:example@localhost:27017/")
    db = myclient["Copernicus"]
    collection_names = ["SENTINEL-1", "SENTINEL-2"]
    for collection_name in collection_names:
        for feature in db[collection_name].find():
            geometry_geojson = feature['geometry']
            if is_valid_geojson_result(geometry_geojson):
                geometry = geojson_to_geosgeom(geometry_geojson)
                sensor_type_str = feature['sensor_type']
                technique = map_sensor_to_technique(sensor_type_str)
                archive_item = ArchiveItem.objects.bulk_create(
                    external_id=feature['id'],
                    geometry=geometry,
                    collection=collection_name,
                    sensor_type=technique,
                    thumbnail=feature['assets']['thumbnail']["href"],
                    start_date=feature['start_date'].replace(tzinfo=timezone.utc),
                    end_date=feature['end_date'].replace(tzinfo=timezone.utc),
                    metadata=str(feature['properties']),
                )

class Command(BaseCommand):

    help = "Pulls all data from the Oracle system"

    def handle(self, *args, **options):
        fetch_from_mongo()
    
    # def handle(self, *args, **options):
        # filepath = Path(__file__).parent / "data" / "test.json"
        # ingest_archive_items(filepath)
    
    # def handle(self, *args, **options):
        
    #     initial_datetime = datetime(year=2014,
    #                                 month=1,
    #                                 day=1
    #                             )
    #     present_datetime = datetime.now()
    #     day_difference = (present_datetime - initial_datetime).days

    #     curr_datetime = datetime(year=initial_datetime.year, month=initial_datetime.month, day=initial_datetime.day)
    #     for day_step in range(1, day_difference // 30):
            
    #         end_date = initial_datetime + timedelta(days=day_step * 30)
    #         print(f"Getting results for {curr_datetime} | {end_date}")
    #         fetch_archive_items(curr_datetime, end_date)
    #         curr_datetime = end_date