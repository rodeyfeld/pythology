
from datetime import timedelta, datetime, timezone
import json
from airflow.decorators import dag, task, task_group
from airflow.operators.python import get_current_context
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
import uuid


def build_execute_query(archive_finder_pk, run_id, run_datetime):
    
    sql = f"""
    CREATE TABLE archive_seeker_{run_id} AS
    SELECT 
        archive_items.id as archive_item_id,
        archive_finders.id as archive_finder_id
    FROM augury_archiveitem archive_items
    LEFT JOIN archive_finder_archivefinder archive_finders
    ON archive_items.start_date >= archive_finders.start_date
    AND archive_items.end_date >= archive_finders.end_date
    WHERE ST_Intersects(
        archive_items.geometry,
        archive_finders.geometry
    )
    AND archive_finders.id = {archive_finder_pk}
    ;

    INSERT INTO archive_finder_archivelookup (created, modified, seeker_id, seeker_datetime, archive_finder_id, archive_item_id)
    SELECT
        CURRENT_TIMESTAMP as created,
        CURRENT_TIMESTAMP as modified,
        {run_id},
        {run_datetime},
        archive_finder_id,
        archive_item_id
    FROM archive_seeker_{run_id}
    ;
    """
    return sql


default_params ={"archive_finder_pk": 2}

@dag(
    schedule=None,
    catchup=False,
    tags=["archive_finder"],
    params=default_params
)
def imagery_finder(run_id):
    """
    Process all archive results
    """

    @task_group
    def etl():

        def get_archive_finder_pk():
            context = get_current_context()
            conf = context["dag_run"].conf
            archive_finder_pk = conf.get("archive_finder_pk")
            return archive_finder_pk

        @task(pool="postgres_pool")
        def create_archive_finder_items():
            archive_finder_pk = get_archive_finder_pk()
            run_datetime = datetime.now().isoformat()
            execute_query = SQLExecuteQueryOperator(
                conn_id="postgres_default",
                task_id=f"execute_archive_finder_{archive_finder_pk}_{run_id}",
                sql=build_execute_query(archive_finder_pk=archive_finder_pk, run_id=run_id, run_datetime=run_datetime),
            )
            execute_query.execute(context={})


        @task
        def notify_augur():
            archive_finder_pk = get_archive_finder_pk()
            
            poll_archive_finder = SimpleHttpOperator(
                http_conn_id="http_augur_connection",
                task_id=f"poll_archive_finder_{archive_finder_pk}_{run_id}",
                endpoint=f"api/archive_finder/finders/study/process/{archive_finder_pk}",
                method="GET",
            )
            poll_archive_finder.execute(context={})

        
        create_archive_finder_items() 
        notify_augur()
        

    etl()

imagery_finder(uuid.uuid4().hex)
