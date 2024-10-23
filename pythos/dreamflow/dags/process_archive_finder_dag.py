
import json

import pendulum

from airflow.decorators import dag, task
from airflow.settings import SQL_ALCHEMY_CONN
from sqlalchemy import create_engine, text


@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["archive_finder"],
)
def process_archive_finder_results():
    """
    Process all archive results
    """
    @task()
    def extract():
        # Create an SQLAlchemy engine using the connection string from airflow.cfg
        engine = create_engine(SQL_ALCHEMY_CONN)

        # Define your SQL query
        query = "SELECT * FROM archive_finder_archivefinder LIMIT 10;"

        with engine.connect() as connection:
            result = connection.execute(text(query))

            # Fetch results
            for row in result:
                print(row)


    extract()



process_archive_finder_results()
