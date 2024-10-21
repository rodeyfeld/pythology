FROM apache/airflow:2.10.2

WORKDIR /dreamflow
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         vim \
         libpq-dev \
  && apt-get autoremove -yqq --purge \
  && apt-get clean 
  
USER airflow
COPY . /dreamflow
# RUN python -m pip install pip-tools
# RUN pip-compile --output-file=requirements.txt pyproject.toml
# RUN pip-compile --constraint=requirements.txt --extra=dev --output-file=dev-requirements.txt
# RUN pip-sync