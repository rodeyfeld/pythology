Setup tools for postgres
docker build --tag atlas .
docker run -p 5432:5432 atlas
echo "export PG_PASSWORD=postgres" > .env


## docker
```
docker run -p 5432:5432 --name atlas -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -d atlas
```

## docker prod
```
echo .env >> .dockerignore
docker build --tag edrodefeld/atlas .
docker push edrodefeld/atlas:latest
```
