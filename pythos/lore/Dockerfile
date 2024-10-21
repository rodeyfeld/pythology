FROM postgis/postgis:16-master

WORKDIR /lore
USER postgres
COPY . /lore
COPY init.sql /docker-entrypoint-initdb.d/