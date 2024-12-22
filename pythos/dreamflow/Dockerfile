FROM apache/airflow:2.10.2

WORKDIR /dreamflow
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         vim \
         libpq-dev \
  && apt-get autoremove -yqq --purge \
  && apt-get clean 
  
COPY . /dreamflow
RUN pip install --upgrade pip pip-tools
RUN pip-compile --output-file=requirements.txt pyproject.toml
RUN pip-sync
