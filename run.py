from hdash.reader.atlas_reader import AtlasReader
from hdash.db.db_util import DbConnection

# Step 0:  Start with Fresh Database
db_connection = DbConnection()
print ("Resetting database.")
db_connection.reset_database()

# Step 1:  Read in the Atlases from Config File
reader = AtlasReader("config/htan_projects.csv")
atlas_list = reader.atlas_list;
print(f"Saving {len(atlas_list)} atlases to the database.")
reader.save_to_database()

########  For each atlas:

# Step 2: Get the Master Table from Synapse

# Step 3: Transform the Master Table into a list of AtlasFiles

# Step 4: Count the Files

# Step 5: Save stats back to the database

# Step 6: Save meta-files to the database

