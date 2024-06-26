"""AtlasFile ORM Class."""
from sqlalchemy import Column, String, BigInteger
from hdash.db.db_base import Base


class AtlasFile(Base):
    """AtlasFile ORM Class."""

    __tablename__ = "atlas_file"
    synapse_id = Column(String(255), primary_key=True)
    atlas_id = Column(String(255))
    name = Column(String(255))
    parent_id = Column(String(255))
    path = Column(String(1024))
    file_type = Column(String(25))
    data_type = Column(String(25))
    category = Column(String(255))
    size_bytes = Column(BigInteger)
    md5 = Column(String(255))
    modified_on = Column(BigInteger)

    def __init__(self):
        """Create Atlas File."""
        self.size_bytes = 0

    def __repr__(self):
        """Get summary."""
        return f"<AtlasFile({self.synapse_id}, {self.data_type})>"
