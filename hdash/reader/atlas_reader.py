"""Atlas Reader."""
from hdash.db.atlas import Atlas
from hdash.db.db_util import DbConnection


class AtlasReader:
    """Read Atlas Data from a CSV and Saves to the Database."""

    def __init__(self, file):
        """Create Atlas Reader Object."""
        fd = open(file)
        self.atlas_list = []
        for line in fd:
            parts = line.split(",")
            atlas = Atlas(parts[1], parts[2], parts[0], parts[3])
            self.atlas_list.append(atlas)

    def save_to_database(self):
        """Save all records to the database."""
        db_connection = DbConnection()
        db_connection.reset_database()
        session = db_connection.session
        for atlas in self.atlas_list:
            session.add(atlas)
        session.commit()
        session.close()
