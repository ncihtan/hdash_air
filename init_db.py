from hdash.reader.atlas_reader import AtlasReader
from hdash.db.db_util import DbConnection

db_connection = DbConnection()
print ("Resetting database.")
db_connection.reset_database()

reader = AtlasReader("config/htan_projects.csv")
atlas_list = reader.atlas_list;
print(f"Saving {len(atlas_list)} atlases to the database.")
reader.save_to_database()
