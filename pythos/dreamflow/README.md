
# dreamflow - Airflow Based DAG Runner


## Local setup

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


## To run
- ```source .env```
- ```airflow standalone```
- Navigate to `localhost:8080`
- Use password provided in logs

### compile settings
This project uses a constraints file required by airflow. 
`pip-compile --output-file=requirements.txt pyproject.toml --constraint constraints.tx`

![image](https://github.com/user-attachments/assets/354aeff0-b957-436a-a557-08c2a690aa4f)
![image](https://github.com/user-attachments/assets/c5072132-440e-41d9-9226-333217844183)

![image](https://github.com/user-attachments/assets/a23a02c8-dce1-4ce0-bd30-dfe6872c01d1)
