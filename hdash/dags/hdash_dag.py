"""
HTAN Dashboard DAG.
"""
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow import DAG
from airflow.decorators import task
from datetime import datetime

# Create the DAG
with DAG(
    dag_id="hdash",
    start_date=datetime(2023,1,1),
    schedule=None,
    catchup=False,
    tags= ["htan"],
) as dag:
    @task()
    def fetch_atlases():
        request = "SELECT * FROM ATLAS"
        mysql_hook = MySqlHook(mysql_conn_id='mysql', schema='htan')
        connection = mysql_hook.get_conn()
        cursor = connection.cursor()
        cursor.execute(request)

        # Records are output to Airflow Log
        id_list = []
        for record in cursor:
            id_list.append((record[0], record[1]))
            print(record)
        connection.close()
        return id_list

    @task
    def get_synapse_data(atlas_id_tuple):
        atlas_id = atlas_id_tuple[0]
        synapse_id = atlas_id_tuple[1]
        print("Getting Synapse data for: " + atlas_id)
        print("Using Synapse ID:  " + synapse_id)

    # Run the DAG
    id_list = fetch_atlases()
    get_synapse_data.expand(atlas_id_tuple = id_list)
