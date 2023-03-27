from hdash.reader.atlas_reader import AtlasReader
from hdash.db.db_util import DbConnection
from hdash.db.atlas import Atlas
from hdash.db.atlas_file import AtlasFile
from hdash.db.atlas_stats import AtlasStats

# Step 0:  Start with Fresh Database
db_connection = DbConnection()
print ("Resetting database.")
db_connection.reset_database()
session = db_connection.session

# Step 1:  Read in the Atlases from Config File
reader = AtlasReader("config/htan_projects.csv")
atlas_list = reader.atlas_list
print(f"Saving {len(atlas_list)} atlases to the database.")
for atlas in atlas_list:
    session.add(atlas)
session.commit()

########  For each atlas:

atlas_list = session.query(Atlas).all()
for atlas in atlas_list:
    print(atlas)

# Step 2: Get the Master Table from Synapse

# Step 3: Transform the Master Table into a list of AtlasFiles

# Step 4: Count the Files

# Step 5: Save stats back to the database

# Step 6: Save meta-files to the database

