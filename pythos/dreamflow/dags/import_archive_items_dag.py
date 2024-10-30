
from airflow.decorators import dag, task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.mongo.hooks.mongo import MongoHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
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
        if geojson['type'] in ("Polygon"):
            if coords := geojson.get('coordinates'):
                if len(coords) > 0:
                    return True
        return False

    def geojson_to_wkt(geojson):
        geometry = shape(geojson)
        return dumps(geometry)

    def map_sensor_to_technique(sensor: str):
        if sensor in ('EO', 'MSI'):
            return 'EO'
        elif sensor in ('SAR'):
            return'SAR'
        return 'UNKNOWN'
    

    all_archive_finders = SQLExecuteQueryOperator(
        conn_id='postgres_default',
        task_id="all_archive_finders",
        sql="sql/all_archive_finders.sql",
        show_return_value_in_logs=True,
    )

    @task
    def postgrestime():
        # hook = PostgresHook(postgres_conn_id='postgres_default')
        print("GETTING RESULTS")
        print(all_archive_finders)
        print("ENDED RESULTS")

    @task
    def mongotime():
        hook = MongoHook(mongo_conn_id='mongo_default')
        client = hook.get_conn()
        db = client["Copernicus"]
        collection_names = ["SENTINEL-1", "SENTINEL-2"]
        
        for collection_name in collection_names:
            for feature in db[collection_name].find():
                geometry_geojson = feature['geometry']
                if is_valid_geometry_type(geometry_geojson):
                    geometry = geojson_to_wkt(geometry_geojson)
                    sensor_type_str = feature['sensor_type']
                    technique = map_sensor_to_technique(sensor_type_str)
                    # archive_item = ArchiveItem.objects.bulk_create(
                    #     external_id=feature['id'],
                    #     geometry=geometry,
                    #     collection=collection_name,
                    #     sensor_type=technique,
                    #     thumbnail=feature['assets']['thumbnail']["href"],
                    #     start_date=feature['start_date'].replace(tzinfo=timezone.utc),
                    #     end_date=feature['end_date'].replace(tzinfo=timezone.utc),
                    #     metadata=str(feature['properties']),
                    # )

    postgrestime()

import_archive_items()
