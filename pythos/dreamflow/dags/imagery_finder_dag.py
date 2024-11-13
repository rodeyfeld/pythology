
from datetime import datetime
import json
from airflow.decorators import dag, task, task_group
from airflow.operators.python import get_current_context
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator


def build_execute_query(archive_finder_pk, dream_pk):
    
    

    sql = f"""

    CREATE TABLE archive_seeker_{archive_finder_pk}_{dream_pk} AS
    SELECT 
        archive_items.id as archive_item_id,
        archive_finders.id as archive_finder_id
    FROM archive_finder_archiveitem archive_items
    LEFT JOIN archive_finder_archivefinder archive_finders
    ON archive_items.start_date >= archive_finders.start_date
    AND archive_items.end_date >= archive_finders.end_date
    WHERE ST_Intersects(
        archive_items.geometry,
        archive_finders.geometry
    )
    AND archive_finders.id = {archive_finder_pk}
    ;

    INSERT INTO archive_finder_imagerylookupitem (created, modified, archive_finder_id, archive_item_id, study_id)
    SELECT
        CURRENT_TIMESTAMP as created,
        CURRENT_TIMESTAMP as modified,
        archive_finder_id,
        archive_item_id,
        (SELECT study_id FROM augury_dream WHERE id = {dream_pk}) as study_id
    FROM archive_seeker_{archive_finder_pk}_{dream_pk}
    ;
    """
    return sql


default_params ={"archive_finder_pk": 2, "dream_pk": 1}

@dag(
    schedule=None,
    catchup=False,
    tags=["archive_finder"],
    params=default_params
)
def imagery_finder():
    """
    Process all archive results
    """

    @task_group
    def etl():

        def get_conf_value(key):
            context = get_current_context()
            conf = context["dag_run"].conf
            return conf.get(key)

        @task(pool="postgres_pool")
        def create_archive_finder_items():
            archive_finder_pk = get_conf_value("archive_finder_pk")
            dream_pk = get_conf_value("dream_pk")

            execute_query = SQLExecuteQueryOperator(
                conn_id="postgres_default",
                task_id=f"execute_archive_finder_{archive_finder_pk}_{dream_pk}",
                sql=build_execute_query(archive_finder_pk=archive_finder_pk, dream_pk=dream_pk),
            )
            execute_query.execute(context={})


        @task
        def notify_augur(_):
            dream_pk = get_conf_value("dream_pk")
            
            poll_archive_finder = SimpleHttpOperator(
                http_conn_id="http_augur_connection",
                task_id=f"notify_diviner_{dream_pk}",
                endpoint=f"api/augury/divine",
                data=json.dumps({"dream_id": dream_pk}),
                method="POST",
            )
            poll_archive_finder.execute(context={})
        
        notify_augur(create_archive_finder_items())
        
    etl()

imagery_finder()
