"""HTAN Dashboard DAG."""
from typing import List
import logging
from datetime import datetime
from datetime import timedelta
from natsort import natsorted
import boto3
from airflow import DAG
from airflow.decorators import task
from hdash.util.s3_credentials import S3Credentials
from hdash.synapse.connector import SynapseConnector
from hdash.db.atlas import Atlas
from hdash.db.db_util import DbConnection
from hdash.synapse.file_counter import FileCounter
from hdash.synapse.atlas_info import AtlasInfo
from hdash.db.atlas_stats import AtlasStats
from hdash.db.atlas_file import AtlasFile
from hdash.db.meta_cache import MetaCache
from hdash.db.matrix import Matrix
from hdash.db.validation import Validation, ValidationError
from hdash.db.web_cache import WebCache
from hdash.synapse.meta_file import MetaFile
from hdash.synapse.meta_map import MetaMap
from hdash.synapse.file_type import FileType
from hdash.validator.htan_validator import HtanValidator
from hdash.graph.sif_writer import SifWriter
from hdash.stats.meta_summary import MetaDataSummary
from hdash.util.web_writer import WebWriter
from hdash.util.matrix_util import MatrixUtil
from hdash.stats.completeness_summary import CompletenessSummary
from hdash.graph.graph_creator import GraphCreator
from hdash.graph.graph_flattener import GraphFlattener
from hdash.util.html_matrix import HtmlMatrix
from hdash.util.slack import Slack


logger = logging.getLogger("airflow.task")


def dag_failure_alert(context):
    """Handle Failure."""
    task_instance_key_str = context["task_instance_key_str"]
    error_msg = f"Failure occurred at: {task_instance_key_str}."
    slack = Slack()
    logger.info("Sending failure message to Slack:  %s.", error_msg)
    response = slack.post_msg(False, error_msg)
    logger.info("Response from Slack:  %s.", response.status_code)


def dag_success_alert(context):
    """Handle Success."""
    run_id = context["run_id"]
    success_msg = f"Run ID Succeeded: {run_id}."
    slack = Slack()
    logger.info("Sending success message to Slack:  %s.", success_msg)
    response = slack.post_msg(True, success_msg)
    logger.info("Response from Slack:  %s.", response.status_code)


# Create the DAG
with DAG(
    dag_id="hdash",
    start_date=datetime(2023, 1, 1),
    schedule="0 0,4,8,12,16,20 * * *",
    catchup=False,
    max_active_runs=1,
    tags=["htan"],
    on_success_callback=dag_success_alert,
    on_failure_callback=dag_failure_alert,
    dagrun_timeout=timedelta(minutes=10)
) as dag:

    @task()
    def get_atlas_list():
        # pylint: disable=unused-argument
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

        # Delete any Existing Matrices
        session.query(Matrix).delete()
        session.commit()

        session.close()
        return id_list

    @task
    def get_atlas_files(atlas_id: str):
        # pylint: disable=unused-argument
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
        # pylint: disable=unused-argument
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
            # Check if meta file is already cached
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
        # pylint: disable=unused-argument
        """Validate atlas and store results to the database."""
        logger.info("Validating atlas:  %s.", atlas_id)
        db_connection = DbConnection()
        session = db_connection.session

        # Validate
        meta_map = _get_meta_map(atlas_id, session)
        graph_creator = GraphCreator(atlas_id, meta_map)
        htan_graph = graph_creator.htan_graph
        validator = HtanValidator(atlas_id, meta_map, htan_graph)

        # Store Validation Results to Database
        validation_list = validator.get_validation_results()
        session.add_all(validation_list)
        session.commit()

        # Assess Completeness of Metadata
        atlas_stats = session.query(AtlasStats).filter_by(atlas_id=atlas_id).one()
        meta_summary = MetaDataSummary(meta_map.meta_list_sorted)
        atlas_stats.percent_metadata_complete = (
            meta_summary.get_overall_percent_complete()
        )
        session.commit()

        # Assess Completeness across Levels
        graph_flat = GraphFlattener(htan_graph)
        completeness_summary = CompletenessSummary("HTA1", meta_map, graph_flat)
        matrix_util = MatrixUtil(atlas_id, completeness_summary)
        matrix_list = matrix_util.matrix_list
        session.add_all(matrix_list)

        # Store SIF Network
        directed_graph = htan_graph.directed_graph
        sif_writer = SifWriter(directed_graph)
        web_cache = WebCache()
        web_cache.file_name = f"{atlas_id}_network.sif"
        web_cache.content = sif_writer.sif
        session.add(web_cache)
        session.commit()
        return atlas_id

    @task
    def create_web(atlas_id_list):
        # pylint: disable=unused-argument
        """Create Web Site."""
        db_connection = DbConnection()
        session = db_connection.session
        atlas_id_list = natsorted(atlas_id_list)
        atlas_info_list = _get_atlas_info_list(atlas_id_list, session)

        web_writer = WebWriter(atlas_info_list)
        web_cache = WebCache()
        web_cache.file_name = "index.html"
        web_cache.content = web_writer.index_html
        logger.info("Creating index.html")
        session.add(web_cache)

        for atlas_id in atlas_id_list:
            atlas_html = web_writer.atlas_html_map[atlas_id]
            web_cache = WebCache()
            web_cache.file_name = f"{atlas_id}.html"
            web_cache.content = atlas_html
            logger.info("Creating %s.", web_cache.file_name)
            session.add(web_cache)
        session.commit()
        return len(atlas_id_list)

    @task
    def deploy_web(deploy_num_atlases):
        # pylint: disable=unused-argument
        """Deploy website to S3 Bucket."""
        if deploy_num_atlases > 0:
            db_connection = DbConnection()
            session = db_connection.session
            s3_credentials = S3Credentials()
            s3_config = s3_credentials.get_s3_config()
            client = boto3.client("s3", **s3_config)
            end_point = f"{s3_credentials.endpoint_url}/{s3_credentials.bucket_name}"
            logger.info("Deploying to:  %s.", end_point)
            web_list = session.query(WebCache).all()
            for web_cache in web_list:
                logger.info("Writing:  %s.", web_cache.file_name)
                client.put_object(
                    Bucket=s3_credentials.bucket_name,
                    Key=web_cache.file_name,
                    Body=web_cache.content,
                    ACL="public-read",
                    ContentType="text/html",
                )

    def _get_meta_map(atlas_id, session):
        """Get the Meta Map Object."""
        meta_map = MetaMap()
        atlas_file_list = (
            session.query(AtlasFile)
            .filter_by(atlas_id=atlas_id, data_type=FileType.METADATA.value)
            .order_by(AtlasFile.category)
            .all()
        )
        for atlas_file in atlas_file_list:
            meta_cache = session.query(MetaCache).filter_by(md5=atlas_file.md5).first()
            meta_map.add_meta_file(MetaFile(atlas_file, meta_cache))
        return meta_map

    def _get_atlas_info_list(atlas_list, session):
        """Get Atlas Info List."""
        atlas_info_list: List[AtlasInfo] = []
        for atlas_id in atlas_list:
            atlas = session.query(Atlas).filter_by(atlas_id=atlas_id).one()
            atlas_stats = session.query(AtlasStats).filter_by(atlas_id=atlas_id).one()
            meta_map = _get_meta_map(atlas_id, session)
            validation_list = (
                session.query(Validation)
                .filter_by(atlas_id=atlas_id)
                .order_by(Validation.validation_order)
                .all()
            )
            matrix_list = (
                session.query(Matrix)
                .filter_by(atlas_id=atlas_id)
                .order_by(Matrix.order)
                .all()
            )
            html_matrix_list = []
            for matrix in matrix_list:
                html_matrix_list.append(HtmlMatrix(matrix))

            atlas_info = AtlasInfo(
                atlas,
                atlas_stats,
                meta_map.meta_list_sorted,
                validation_list,
                html_matrix_list,
            )
            atlas_info_list.append(atlas_info)
        return atlas_info_list

    # Run the DAG
    atlas_id_list1 = get_atlas_list()
    atlas_id_list2 = get_atlas_files.expand(atlas_id=atlas_id_list1)
    atlas_id_list3 = get_meta_files.expand(atlas_id=atlas_id_list2)
    atlas_id_list4 = validate_atlas.expand(atlas_id=atlas_id_list3)
    num_atlases = create_web(atlas_id_list4)
    deploy_web(num_atlases)
