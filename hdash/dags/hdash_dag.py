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
from hdash.db.atlas_file import AtlasFile
from hdash.db.meta_cache import MetaCache
from hdash.db.validation import Validation, ValidationError
from hdash.db.web_cache import WebCache
from hdash.synapse.meta_file import MetaFile
from hdash.synapse.meta_map import MetaMap
from hdash.synapse.file_type import FileType
from hdash.validator.htan_validator import HtanValidator
from hdash.graph.graph_creator import GraphCreator
from hdash.graph.sif_writer import SifWriter
from hdash.stats.meta_summary import MetaDataSummary


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

        # Delete any Existing Atlas Stats Records
        session.query(AtlasStats).delete()
        session.commit()

        # Delete any Existing Atlas Files
        session.query(AtlasFile).delete()
        session.commit()

        # Delete any Existing Validation Results
        session.query(ValidationError).delete()
        session.query(Validation).delete()
        session.commit()

        # Delete any Existing Web Resources
        session.query(WebCache).delete()
        session.commit()

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

        # Save stats back to the database
        file_counter = FileCounter(file_list)
        stats = AtlasStats(atlas.atlas_id)
        stats.total_file_size = file_counter.get_total_file_size()
        stats.num_bam_files = file_counter.get_num_files(FileType.BAM.value)
        stats.num_fastq_files = file_counter.get_num_files(FileType.FASTQ.value)
        stats.num_image_files = file_counter.get_num_files(FileType.IMAGE.value)
        stats.num_matrix_files = file_counter.get_num_files(FileType.MATRIX.value)
        stats.num_other_files = file_counter.get_num_files(FileType.OTHER.value)
        print("Saving stats to database")
        session.add(stats)
        session.commit()

        # Save Files to Database
        if len(file_list) > 0:
            session.add_all(file_list)
            session.commit()
        return atlas_id

    @task
    def get_meta_files(atlas_id: str):
        """Get all meta files and store contents in database."""
        db_connection = DbConnection()
        session = db_connection.session
        atlas = session.query(Atlas).filter_by(atlas_id=atlas_id).one()
        logger.info("Getting Metadata files for:  %s.", atlas)

        meta_list = (
            session.query(AtlasFile)
            .filter_by(atlas_id=atlas_id, data_type=FileType.METADATA.value)
            .all()
        )
        logger.info("Processing %d meta files.", len(meta_list))

        connector = SynapseConnector()
        for meta_file in meta_list:
            # Check that meta file is already cached
            cache = session.query(MetaCache).filter_by(md5=meta_file.md5).first()
            if cache is None:
                logger.info("Retrieving meta file:  %s", meta_file.synapse_id)
                csv = connector.get_cvs_table(meta_file.synapse_id)
                meta_cache = MetaCache()
                meta_cache.synapse_id = meta_file.synapse_id
                meta_cache.md5 = meta_file.md5
                meta_cache.content = csv
                session.add(meta_cache)
                session.commit()
            else:
                logger.info("Skipping. Found cache for:  %s", meta_file.synapse_id)
        return atlas_id

    @task
    def validate_atlas(atlas_id: str):
        """Validate atlas and store results to the database."""
        logger.info("Valdating atlas:  %s.", atlas_id)
        db_connection = DbConnection()
        session = db_connection.session

        # Create the metamap
        meta_map = MetaMap()
        atlas_file_list = (
            session.query(AtlasFile)
            .filter_by(atlas_id=atlas_id, data_type=FileType.METADATA.value)
            .all()
        )
        for atlas_file in atlas_file_list:
            meta_cache = session.query(MetaCache).filter_by(md5=atlas_file.md5).first()
            meta_map.add_meta_file(MetaFile(atlas_file, meta_cache))

        # Validate
        graph_creator = GraphCreator(atlas_id, meta_map)
        htan_graph = graph_creator.htan_graph
        validator = HtanValidator(atlas_id, meta_map, htan_graph)

        # Store Validation Results to Database
        validation_list = validator.get_validation_results()
        session.add_all(validation_list)
        session.commit()

        # Assess Completeness
        atlas_stats = session.query(AtlasStats).filter_by(atlas_id=atlas_id).one()
        meta_summary = MetaDataSummary(meta_map.meta_list_sorted)
        atlas_stats.percent_metadata_complete = (
            meta_summary.get_overall_percent_complete()
        )
        session.commit()

        # Store SIF Network
        directed_graph = htan_graph.directed_graph
        sif_writer = SifWriter(directed_graph)
        web_cache = WebCache()
        web_cache.file_name = f"{atlas_id}_network.sif"
        web_cache.content = sif_writer.sif
        session.add(web_cache)
        session.commit()

    # Run the DAG
    atlas_id_list1 = get_atlas_list()
    atlas_id_list2 = get_atlas_files.expand(atlas_id=atlas_id_list1)
    atlas_id_list3 = get_meta_files.expand(atlas_id=atlas_id_list2)
    validate_atlas.expand(atlas_id=atlas_id_list3)
