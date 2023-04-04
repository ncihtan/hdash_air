import sys
from hdash.reader.atlas_reader import AtlasReader
from hdash.db.db_util import DbConnection
from hdash.db.atlas import Atlas
from hdash.synapse.file_type import FileType
from hdash.synapse.connector import SynapseConnector
from hdash.synapse.file_counter import FileCounter
from hdash.db.atlas_file import AtlasFile
from hdash.db.atlas_stats import AtlasStats
from hdash.db.meta_cache import MetaCache
from hdash.db.validation import Validation, ValidationError
from hdash.db.web_cache import WebCache

# Start with Fresh Database
db_connection = DbConnection()
print ("Resetting database.")
db_connection.reset_database()
session = db_connection.session

# Read in the Atlases from Config File
reader = AtlasReader("config/htan_projects.csv")
atlas_list = reader.atlas_list
print(f"Saving {len(atlas_list)} atlases to the database.")
for atlas in atlas_list:
    session.add(atlas)
session.commit()
sys.exit(1)

# Process each atlas
atlas_list = session.query(Atlas).all()
for atlas in atlas_list:
    print(atlas)

    # Get the Master Table from Synapse
    synapse_connector = SynapseConnector()
    file_list = synapse_connector.get_atlas_files(atlas.atlas_id, atlas.synapse_id)

    # Count the Files
    print(f"Total number of files:  {len(file_list)}")
    file_counter = FileCounter(file_list)

    # Save stats back to the database
    stats = AtlasStats(atlas.atlas_id)
    stats.total_file_size = file_counter.get_total_file_size()
    stats.num_bam_files = file_counter.get_num_files(FileType.BAM)
    stats.num_fastq_files = file_counter.get_num_files(FileType.FASTQ)
    stats.num_image_files = file_counter.get_num_files(FileType.IMAGE)
    stats.num_matrix_files = file_counter.get_num_files(FileType.MATRIX)
    stats.num_other_files = file_counter.get_num_files(FileType.OTHER)
    print(f"Save stats to database")
    session.add(stats)
    session.commit()

    # Save meta-files to the database

