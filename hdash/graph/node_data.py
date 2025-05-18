"""Node Data."""
from hdash.synapse.meta_file import MetaFile
from hdash.util.categories import Categories


class NodeData:
    """Node Data."""

    node_id: str
    meta_file: MetaFile

    def __init__(self, node_id: str, meta_file: MetaFile):
        """Create NodeData Object."""
        self.node_id = node_id
        self.meta_file = meta_file
        self.abbrev_map = Categories().abbrev_category_map

    @property
    def sif_id(self):
        """Return Cytoscape SIF ID."""
        return self.abbrev_map[self.meta_file.atlas_file.category] + "_" + self.node_id

    def __repr__(self):
        """Get node summary."""
        return f"Node: {self.node_id}: {self.meta_file.atlas_file.category}"
