"""
HTAN Dashboard DAG.
"""
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow import DAG
from airflow.decorators import task
from datetime import datetime
from hdash.synapse.connector import SynapseConnector
import logging

logger = logging.getLogger("airflow.task")

# Create the DAG
with DAG(
    dag_id="hdash",
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
    tags=["htan"],
) as dag:

    @task()
    def fetch_atlases():
        """
        Fetch all HTAN Atlases from the Database.
        """
        logger.info("Querying database for all atlases")
        request = "SELECT * FROM ATLAS"
        mysql_hook = MySqlHook(mysql_conn_id="mysql", schema="htan")
        connection = mysql_hook.get_conn()
        cursor = connection.cursor()
        cursor.execute(request)

        # Records are output to Airflow Log
        id_list = []
        for record in cursor:
            id_list.append((record[0], record[1]))
            logger.info(record)
        connection.close()
        return id_list

    @task
    def summarize_synapse_files(atlas_id_tuple):
        """
        Summarize all Synapse Files for the Specified Atlas.
        """
        atlas_id = atlas_id_tuple[0]
        synapse_id = atlas_id_tuple[1]
        logger.info("Getting Synapse data:  %s [%s]." % (atlas_id, synapse_id))
        connector = SynapseConnector()
        df = connector.retrieve_atlas_table(synapse_id)

    # Run the DAG
    id_list = fetch_atlases()
    summarize_synapse_files.expand(atlas_id_tuple=id_list)