
import json

import pendulum
import requests

from airflow.decorators import dag, task
from airflow.settings import SQL_ALCHEMY_CONN
from sqlalchemy import create_engine, text
from archive_finder.utils import geojson_to_geosgeom, is_valid_geometry_type
from core.models import IntegrationConfigOption, InternalIntegration, SensorType
from archive_finder.schema import ArchiveResultSeekerAudienceResponseSchema, ArchiveFinderSeekerAudienceRequestSchema

    
@staticmethod
def format_datetime(datetime) -> str:
    return datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    

@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["archive_finder"],
)
def import_archive_items():
    """
    Process all archive results
    """
    @task()
    def extract():
   
    def map_sensor_to_technique(self, sensor: str):
        if sensor in ('EO', 'MSI'):
            return SensorType.TechniqueChoices.EO
        elif sensor in ('SAR'):
            return SensorType.TechniqueChoices.SAR
        print(f"{sensor=}")
        return SensorType.TechniqueChoices.UNKNOWN


    def create_archive_results(self, seeker_results: ArchiveResultSeekerAudienceResponseSchema):
        seeker_run_id = seeker_results.id
        for catalog in seeker_results.catalogs:
            catalog_name = catalog['name']
            provider, _ = Provider.objects.get_or_create(
                name=catalog_name
            )
            for catalog_collection in catalog['collections']:
                collection_name = catalog_collection['name']
                features = catalog_collection['features'] if catalog_collection['features'] else []
                for feature in features:
                    geometry_geojson = feature['geometry']
                    if self.is_valid_geojson_result(geometry_geojson):
                        geometry = geojson_to_geosgeom(geometry_geojson)

                        sensor_type_str = feature['sensor_type']
                        technique = self.map_sensor_to_technique(sensor_type_str)
                        sensor_type, _ = SensorType.objects.get_or_create(
                            technique=technique
                        )
                        archive_result = ArchiveItem.create(
                            sensor_type=sensor_type,
                            external_id=feature['id'],
                            geometry=geometry,
                            collection=collection_name,
                            thumbnail=feature['assets']['thumbnail']["href"],
                            start_date=feature['start_date'],
                            end_date=feature['end_date'],
                            metadata=str(feature['properties']),
                            )

    def get_archive_results(self):

        payload = ArchiveFinderSeekerAudienceRequestSchema(
            archive_finder_id=self.archive_finder.pk,
            start_date=f"{Seeker.format_date(self.archive_finder.start_date)}", 
            end_date=f"{Seeker.format_date(self.archive_finder.end_date)}", 
            sortby="datetime",
        )
        payload_json = payload.model_dump_json()
        
        stac_endpoint_config = self.internal_integration.config_options.all().get(key=IntegrationConfigOption.ConfigFieldChoices.STAC_ENDPOINT)
        url = stac_endpoint_config.value
        response = requests.post(url=url, json=payload_json)
        response_data = response.json()
        seeker_results = ArchiveResultSeekerAudienceResponseSchema(
            archive_finder_id=response_data['archive_finder_id'],
            id=response_data['id'],
            catalogs=response_data['catalogs']
        )
        self.create_archive_results(seeker_results=seeker_results)


process_archive_finder_results()
