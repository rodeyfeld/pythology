
from datetime import timedelta, datetime, timezone
from airflow.decorators import dag, task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.mongo.hooks.mongo import MongoHook
from shapely.geometry import shape
from shapely.geometry import shape
from shapely.wkt import dumps
    
@staticmethod
def format_datetime(datetime) -> str:
    return datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

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

@dag(
    schedule=None,
    catchup=False,
    tags=["archive_finder"],
)
def import_archive_items():
    """
    Process all archive results
    """

    def insert_to_postgres(archive_items):
        # hook = PostgresHook(postgres_conn_id='postgres_default')
        for archive_item in archive_items:
            print(archive_item)    
            inserted_archive_items = SQLExecuteQueryOperator(
                conn_id='postgres_default',
                task_id="all_archive_finders",
                sql="sql/insert_archiove_items.sql",
                parameters=archive_items,
                show_return_value_in_logs=True,
            )
            inserted_archive_items

    def fetch_from_mongo(date_range):
        hook = MongoHook(mongo_conn_id='mongo_default')
        client = hook.get_conn()
        db = client["Copernicus"]
        collection_names = ["SENTINEL-1", "SENTINEL-2"]
        
        archive_items = []
        for collection_name in collection_names:
            features = db[collection_name].find(
                {
                    'start_date': {"$gt": date_range['start_date']},
                    'end_date': {"$lte": date_range['end_date']},
                }
            )
            for feature in features:
                geometry_geojson = feature['geometry']
                if is_valid_geometry_type(geometry_geojson):
                    geometry = geojson_to_wkt(geometry_geojson)
                    sensor_type_str = feature['sensor_type']
                    technique = map_sensor_to_technique(sensor_type_str)
                    archive_item = {
                        "external_id" : feature['id'],
                        "geometry" : geometry,
                        "collection" : collection_name,
                        "sensor_type" : technique,
                        "thumbnail" : feature['assets']['thumbnail']["href"],
                        "start_date" : feature['start_date'].replace(tzinfo=timezone.utc),
                        "end_date" : feature['end_date'].replace(tzinfo=timezone.utc),
                        "metadata" : str(feature['properties']),
                    }

                    archive_items.append(archive_item)
        return archive_items

    @task
    def get_date_ranges():
        initial_datetime = datetime(year=2014,
                                    month=1,
                                    day=1,
                                    second=1
                                )
        present_datetime = datetime(year=2015,
                                    month=1,
                                    day=1,
                                    second=1
                                )
        # present_datetime = datetime.now()
        day_difference = (present_datetime - initial_datetime).days

        curr_datetime = datetime(year=initial_datetime.year, month=initial_datetime.month, day=initial_datetime.day)
        date_ranges = []
        for day_step in range(1, day_difference // 30):
            end_date = initial_datetime + timedelta(days=day_step * 30)
            print(f"Getting results for {curr_datetime} | {end_date}")
            date_ranges.append({
                'start_date': curr_datetime, 
                'end_date': end_date, 
            })
            curr_datetime = end_date
        return date_ranges


    @task
    def consumer(date_range):
        mongo_archive_items = fetch_from_mongo(date_range)
        insert_to_postgres(mongo_archive_items)

    date_ranges = get_date_ranges()
    consumer.expand(date_range=date_ranges)

import_archive_items()
