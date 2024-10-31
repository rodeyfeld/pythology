
from datetime import timedelta, datetime, timezone
import json
from airflow.decorators import dag, task, task_group
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.mongo.hooks.mongo import MongoHook
from shapely.geometry import shape
from shapely.geometry import shape
from shapely.wkt import dumps
    
@staticmethod
def format_datetime(datetime) -> str:
    return datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


    # INSERT INTO "augury_archiveitem" 
    # (
    #     "created",
    #     "modified",
    #     "external_id",
    #     "provider",
    #     "geometry",
    #     "collection",
    #     "sensor_type",
    #     "thumbnail",
    #     "start_date",
    #     "end_date",
    #     "metadata"
    # )
    # VALUES (
    #     CURRENT_TIMESTAMP,
    #     CURRENT_TIMESTAMP,
    #     'copernicus',        
    #     'S1A_IW_GRDH_1SSV_20150106T000528_20150106T000557_004043_004E0B_7D52_COG.SAFE', 
    #     ST_GeomFromText('POLYGON ((92.3164825439453125 45.7546157836914062, 89.0541152954101562 46.1506271362304688, 89.4433212280273438 47.8846588134765625, 92.8128738403320312 47.4881668090820312, 92.3164825439453125 45.7546157836914062))'),  -- String value for geometry
    #     'SENTINEL-1', 
    #     'SAR',  
    #     'https://catalogue.dataspace.copernicus.eu/odata/v1/Assets(be736ab9-f336-4bb4-ac93-c377385562c6)/$value', 
    #     '2015-01-06T00:05:28.320000+00:00',  
    #     '2015-01-06T00:05:57.254000+00:00',
    #     'test_mata'

    # );
def build_insert_query(archive_item):
    sql = f"""
    INSERT INTO "augury_archiveitem" 
    (
        "created",
        "modified",
        "external_id",
        "provider",
        "geometry",
        "collection",
        "sensor_type",
        "thumbnail",
        "start_date",
        "end_date",
        "metadata"
    )
    VALUES (
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP,
        '{archive_item["external_id"]}', 
        '{archive_item["provider"]}',
        ST_GeomFromText('{archive_item["geometry"]}'),
        '{archive_item["collection"]}',  
        '{archive_item["sensor_type"]}',  
        '{archive_item["thumbnail"]}', 
        '{archive_item["start_date"].isoformat()}', 
        '{archive_item["end_date"].isoformat()}',
        '{archive_item["metadata"]}'
    );
    """
    return sql

def is_valid_geometry_type(geojson):
    if geojson["type"] in ("Polygon"):
        if coords := geojson.get("coordinates"):
            if len(coords) > 0:
                return True
    return False

def geojson_to_wkt(geojson):
    geometry = shape(geojson)
    return dumps(geometry)

def map_sensor_to_technique(sensor: str):
    if sensor in ("EO", "MSI"):
        return "EO"
    elif sensor in ("SAR"):
        return"SAR"
    return "UNKNOWN"

@dag(
    schedule=None,
    catchup=False,
    tags=["archive_finder"],
)
def import_archive_items():
    """
    Process all archive results
    """

    @task_group
    def etl(date_range):
            

        @task
        def insert_to_postgres(archive_items):
            # hook = PostgresHook(postgres_conn_id='postgres_default')
            for archive_item in archive_items[:5]:
                sql_query = build_insert_query(archive_item)
                print(sql_query)
                insert_task = SQLExecuteQueryOperator(
                    conn_id="postgres_default",
                    task_id=f"insert_archive_item_{archive_item.get('external_id')}",
                    sql=sql_query,
                    show_return_value_in_logs=True,
                )
                insert_task.execute(context={})

        @task
        def fetch_from_mongo(date_range):
            hook = MongoHook(mongo_conn_id="mongo_default")
            client = hook.get_conn()
            db = client["Copernicus"]
            collection_names = ["SENTINEL-1", "SENTINEL-2"]
            
            archive_items = []
            for collection_name in collection_names:
                features = db[collection_name].find(
                    {
                        "start_date": {"$gt": date_range["start_date"]},
                        "end_date": {"$lte": date_range["end_date"]},
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
                            "provider": "copernicus",
                            "geometry" : geometry,
                            "collection" : collection_name,
                            "sensor_type" : technique,
                            "thumbnail" : feature['assets']['thumbnail']["href"],
                            "start_date" : feature['start_date'].replace(tzinfo=timezone.utc),
                            "end_date" : feature['end_date'].replace(tzinfo=timezone.utc),
                            "metadata" : json.dumps(feature['properties']),
                        }

                        archive_items.append(archive_item)
            print(f"Archive Item Count: {len(archive_items)}")
            return archive_items
        
        insert_to_postgres(fetch_from_mongo(date_range))

    @task
    def get_date_ranges():
        initial_datetime = datetime(year=2015,
                                    month=1,
                                    day=1,
                                    second=1
                                )
        present_datetime = datetime(year=2015,
                                    month=6,
                                    day=1,
                                    second=1
                                )
        # present_datetime = datetime.now()
        day_difference = (present_datetime - initial_datetime).days

        curr_datetime = datetime(year=initial_datetime.year, month=initial_datetime.month, day=initial_datetime.day)
        date_ranges = []
        stepper = 30
        for day_step in range(1, day_difference // stepper):
            end_date = initial_datetime + timedelta(days=day_step * stepper)
            print(f"Getting results for {curr_datetime} | {end_date}")
            date_ranges.append({
                "start_date": curr_datetime, 
                "end_date": end_date, 
            })
            curr_datetime = end_date
        return date_ranges

    date_ranges = get_date_ranges()
    etl.expand(date_range=date_ranges)

import_archive_items()
