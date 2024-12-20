FROM postgis/postgis:16-master

WORKDIR /atlas
USER postgres

#ARG PG_USER
#ARG PG_PASSWORD

#ENV POSTGRES_USER=${PG_USER}
#ENV POSTGRES_PASSWORD=${PG_PASSWORD}

COPY . /atlas
COPY init.sql /docker-entrypoint-initdb.d/
