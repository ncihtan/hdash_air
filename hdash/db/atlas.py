"""Atlas ORM Class."""

from sqlalchemy import Column, String
from hdash.db.db_base import Base
from typing import Union


class Atlas(Base):
    """Atlas ORM Class."""

    __tablename__ = "atlas"

    atlas_id: Union[str, Column] = Column(String(25), primary_key=True)
    synapse_id: Union[str, Column] = Column(String(100), unique=True)
    name: Union[str, Column] = Column(String(255))
    dcc_liaison: Union[str, Column] = Column(String(255))

    def __init__(self, atlas_id, name, synapse_id, dcc_liaison):
        """Create Atlas Object."""
        self.atlas_id = atlas_id
        self.name = name
        self.synapse_id = synapse_id
        self.dcc_liaison = dcc_liaison

    def __repr__(self):
        """Get summary."""
        return f"<Atlas({self.atlas_id}, {self.name})>"
