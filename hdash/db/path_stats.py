"""Path ORM Class."""
from sqlalchemy import Column, String, Integer
from hdash.db.db_base import Base


class PathStats(Base):
    """PathStats ORM Class."""

    __tablename__ = "path_stats"
    path_stats_id = Column(Integer, primary_key=True, autoincrement=True)
    atlas_id = Column(String(25))
    synapse_id = Column(String(255))
    path = Column(String(1024))
    num_annotated_files = Column(Integer)
    num_un_annotated_files = Column(Integer)

    def __init__(self, atlas_id, synapse_id, path):
        """Create AtlasStats Object."""
        self.atlas_id = atlas_id
        self.synapse_id = synapse_id
        self.path = path
        self.num_annotated_files = 0
        self.num_un_annotated_files = 0

    def __repr__(self):
        """Get summary."""
        return f"<PathStats({self.atlas_id}, {self.path})>"
