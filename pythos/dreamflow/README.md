
### create .env file 
```
export AIRFLOW_UID=1000
export AIRFLOW_PROJ_DIR=$HOME/universe/pythology/pythos/dreamflow
export AIRFLOW_HOME=$HOME/universe/pythology/pythos/dreamflow
export AIRFLOW_CONN_MONGO_DEFAULT=mongodb://root:example@localhost:27017/
export AIRFLOW_CONN_POSTGRES_DEFAULT=postgresql://airflow:airflow@localhost:5432/lore
```

### required libraries
`sudo apt-get install graphviz`


### compile settings
This project uses a constraints file required by airflow. 
`pip-compile --output-file=requirements.txt pyproject.toml --constraint constraints.tx`
