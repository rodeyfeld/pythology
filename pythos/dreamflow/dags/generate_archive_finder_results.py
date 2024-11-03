
from datetime import timedelta, datetime, timezone
import json
from airflow.decorators import dag, task, task_group

from airflow.operators.python import get_current_context
from airflow.models.param import Param
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator


import uuid

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


def build_select_query(archive_finder_pk):
    sql = f"""
    SELECT 
        a_f_af.start_date,
        a_f_af.end_date,
        a_f_af.geometry,
        a_f_af.start_date
    FROM archive_finder_archivefinder a_f_af
    WHERE a_f_af.id = {archive_finder_pk}
    ;
    """
    return sql



def build_execute_query(archive_finder):
    sql = f"""
    CREATE TABLE "augury_archiveitem_{archive_finder["pk"]}" AS
    SELECT a_ai.* 
    FROM augury_archiveitem a_ai
    WHERE a_ai.start_date >= '{archive_finder["start_date"]}'
    AND a_ai.end_date >= '{archive_finder["end_date"]}'
    AND ST_Intersects(
        '{archive_finder["geometry"]}',
          a_ai.geometry
    )
    ;
    """
    return sql


default_params ={"archive_finder_pk": -1}

@dag(
    schedule=None,
    catchup=False,
    tags=["archive_finder"],
    params=default_params
)
def execute_archive_finder():
    """
    Process all archive results
    """


    @task(pool="postgres_pool")
    def generate_archive_finder_results():
        context = get_current_context()
        conf = context["dag_run"].conf
        archive_finder_pk = conf.get("archive_finder_pk")

        select_query =  SQLExecuteQueryOperator(
            conn_id="postgres_default",
            task_id=f"select_archive_finder_{archive_finder_pk}_{uuid.uuid4().hex}",
            sql=build_select_query(archive_finder_pk=archive_finder_pk),
        )  

        execute_query = SQLExecuteQueryOperator(
            conn_id="postgres_default",
            task_id=f"execute_archive_finder_{archive_finder_pk}_{uuid.uuid4().hex}",
            sql=build_execute_query(archive_finder=select_query.output),
        )

        select_query >> execute_query

    generate_archive_finder_results()


execute_archive_finder()
