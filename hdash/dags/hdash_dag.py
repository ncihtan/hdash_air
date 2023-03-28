"""HTAN Dashboard DAG."""
import logging
from datetime import datetime
from airflow import DAG
from airflow.decorators import task
from hdash.synapse.connector import SynapseConnector
from hdash.db.atlas import Atlas
from hdash.db.db_util import DbConnection
from hdash.synapse.file_counter import FileCounter
from hdash.db.atlas_stats import AtlasStats
from hdash.synapse.file_type import FileType


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
    def get_atlas_list():
        """Get all HTAN Atlases from the Database."""
        logger.info("Querying database for all atlases")
        db_connection = DbConnection()
        session = db_connection.session
        atlases = session.query(Atlas).all()
        logger.info("Got %d atlases.", len(atlases))
        id_list = [atlas.atlas_id for atlas in atlases]
        session.close()
        return id_list

    @task
    def get_atlas_files(atlas_id: str):
        """Get all Synapse Files for the Specified Atlas."""
        db_connection = DbConnection()
        session = db_connection.session
        atlas = session.query(Atlas).filter_by(atlas_id=atlas_id).one()

        logger.info("Getting Synapse data:  %s.", atlas)
        connector = SynapseConnector()
        file_list = connector.get_atlas_files(atlas.atlas_id, atlas.synapse_id)

        # Count the Files
        print(f"Total number of files:  {len(file_list)}")

        if len(file_list) > 0:
            file_counter = FileCounter(file_list)

            # Save stats back to the database
            stats = AtlasStats(atlas.atlas_id)
            stats.total_file_size = file_counter.get_total_file_size()
            stats.num_bam_files = file_counter.get_num_files(FileType.BAM)
            stats.num_fastq_files = file_counter.get_num_files(FileType.FASTQ)
            stats.num_image_files = file_counter.get_num_files(FileType.IMAGE)
            stats.num_matrix_files = file_counter.get_num_files(FileType.MATRIX)
            stats.num_other_files = file_counter.get_num_files(FileType.OTHER)
            print(f"Saving stats to database")
            session.add(stats)
            session.commit()

    # Run the DAG
    id_list = get_atlas_list()
    get_atlas_files.expand(atlas_id=id_list)
