FROM postgis/postgis:16-master

WORKDIR /atlas

COPY . /atlas
COPY init.sql /docker-entrypoint-initdb.d/
