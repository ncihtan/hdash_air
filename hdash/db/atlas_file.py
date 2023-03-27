"""AtlasFile ORM Class."""
from sqlalchemy import Column, String, Integer, Boolean
from hdash.db.db_base import Base


class AtlasFile(Base):
    """AtlasFile ORM Class."""

    __tablename__ = "atlas_file"
    synapse_id = Column(String(255), primary_key=True)
    atlas_id = Column(String(255))
    name = Column(String(255))
    parent_id = Column(String(255))
    file_type = Column(String(25))
    data_type = Column(String(25))
    component = Column(String(255))
    size_bytes = Column(Integer)
    is_archive_folder = Column(Boolean)
    is_meta_file = Column(Boolean)
    md5 = Column(String(255))

    def __init__(self):
        """Create Atlas File."""
        self.is_archive_folder = False
        self.is_meta_file = False

    def __repr__(self):
        """Get atlas file summary."""
        return f"<AtlasFile({self.synapse_id}, {self.data_type})>"
