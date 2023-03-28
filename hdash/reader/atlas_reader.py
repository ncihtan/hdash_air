"""Atlas Reader."""
from hdash.db.atlas import Atlas


class AtlasReader:
    """Read Atlas Data from a CSV and Saves to the Database."""

    def __init__(self, file):
        """Create Atlas Reader Object."""
        fd = open(file)
        self.atlas_list = []
        fd.readline()  # Skip header row
        for line in fd:
            parts = line.split(",")
            atlas = Atlas(parts[1], parts[2], parts[0], parts[3])
            self.atlas_list.append(atlas)
