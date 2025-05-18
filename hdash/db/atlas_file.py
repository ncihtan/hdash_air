"""AtlasFile ORM Class."""
from sqlalchemy import Column, String, BigInteger
from hdash.db.db_base import Base
from typing import Union


class AtlasFile(Base):
    """AtlasFile ORM Class."""

    __tablename__ = "atlas_file"
    synapse_id: Union[str, Column] = Column(String(255), primary_key=True)
    atlas_id: Union[str, Column] = Column(String(255))
    name: Union[str, Column] = Column(String(255))
    parent_id: Union[str, Column] = Column(String(255))
    path: Union[str, Column] = Column(String(1024))
    file_type: Union[str, Column] = Column(String(25))
    data_type: Union[str, Column] = Column(String(25))
    category: Union[str, Column] = Column(String(255))
    size_bytes = Column(BigInteger)
    md5: Union[str, Column] = Column(String(255))
    modified_on = Column(BigInteger)

    def __init__(self):
        """Create Atlas File."""
        self.size_bytes = 0

    def __repr__(self):
        """Get summary."""
        return f"<AtlasFile({self.synapse_id}, {self.data_type})>"
