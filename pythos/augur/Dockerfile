FROM python:3.11 

WORKDIR /augur
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         vim \
         gdal-bin \
          libgdal-dev \ 
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
COPY . /augur

RUN python -m pip install pip-tools
RUN pip-compile --output-file=requirements.txt pyproject.toml
RUN pip-compile --constraint=requirements.txt --extra=dev --output-file=dev-requirements.txt
RUN pip-sync
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]