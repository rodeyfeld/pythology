
### create .env file 
```
export AIRFLOW_UID=1000
export AIRFLOW_PROJ_DIR=$HOME/universe/pythology/pythos/dreamflow
export AIRFLOW_HOME=$HOME/universe/pythology/pythos/dreamflow
export AIRFLOW_CONN_MONGO_DEFAULT=mongodb://root:example@localhost:27017/
export AIRFLOW_CONN_POSTGRES_DEFAULT=postgresql+psycopg2://airflow:airflow@localhost:5432/lore
```

`sudo apt-get install graphviz`
`source .env`
`/usr/bin/python3.11 -m venv venv_dreamflow`
`source venv_dreamflow/bin/activate`
`python -m pip install pip-tools`
`pip-sync`


## compile settings
This project uses a constraints file. 
`pip-compile --output-file=requirements.txt pyproject.toml --constraint constraints.tx`
