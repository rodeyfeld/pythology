# AUGUR
REST API for effectively managing user feasibility and archive search requests.


## Docker Setup
```
docker compose up --build
```

Docs are auto generated and hosted at 
- http://127.0.0.1:8000/api/docs


## local postgres setup

Place this file in your home directory ```~/.pg_passfile```, add the following contents:
```
localhost:5432:augur:postgres:mypassyword
```

Place this file in your home directory ```~/.pg_service.conf```, add the following contents:
```
[augur_db_service]
host=localhost
port=5432
dbname=augur
user=postgres
```

Ensure the permissions for both .pg_passfile and .pg_service.conf are set correctly:
```
chmod 600 ~/.pg_passfile
chmod 600 ~/.pg_service.conf
```


## local setup

Run the commands found in the base README.md to activate virtualenvironment.

```
python manage.py migrate
python manage.py runserver
```