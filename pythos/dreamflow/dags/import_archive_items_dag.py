
from airflow.decorators import dag, task
from airflow.settings import SQL_ALCHEMY_CONN
from sqlalchemy import create_engine, text
from shapely.geometry import shape
from shapely.geometry import shape
from shapely.wkt import dumps
    
@staticmethod
def format_datetime(datetime) -> str:
    return datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    

@dag(
    schedule=None,
    catchup=False,
    tags=["archive_finder"],
)
def import_archive_items():
    """
    Process all archive results
    """

    def is_valid_geometry_type(geojson):
        if geojson['type'] in ("MultiPolygon",  "Polygon", "Point"):
            return True
        return False

    def geojson_to_wkt(geojson):
        geometry = shape(geojson)
        return dumps(geometry)

    @task()
    def map_sensor_to_technique(sensor: str):
        if sensor in ('EO', 'MSI'):
            return 'EO'
        elif sensor in ('SAR'):
            return'SAR'
        return 'UNKNOWN'

    @task()
    def create_archive_items(seeker_results: ArchiveResultSeekerAudienceResponseSchema):
        archive_results = []
        for catalog in seeker_results.catalogs:
            catalog_name = catalog['name']
            provider =catalog_name
            for catalog_collection in catalog['collections']:
                collection_name = catalog_collection['name']
                features = catalog_collection['features'] if catalog_collection['features'] else []
                for feature in features:
                    geometry_geojson = feature['geometry']
                    if is_valid_geometry_type(geometry_geojson):
                        wkt = geojson_to_wkt(geometry_geojson)

                        sensor_type_str = feature['sensor_type']
                        technique = map_sensor_to_technique(sensor_type_str)
                        archive_result = ArchiveItem.create(
                            technique=technique,
                            external_id=feature['id'],
                            geometry=geometry,
                            collection=collection_name,
                            thumbnail=feature['assets']['thumbnail']["href"],
                            start_date=feature['start_date'],
                            end_date=feature['end_date'],
                            metadata=str(feature['properties']),
                            )
                        archive_results.append(archive_result)

    def get_archive_results():

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
        create_archive_items(seeker_results=seeker_results)


import_archive_items()
