"""MetaCache ORM Class."""

from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.dialects.mysql import LONGTEXT
from hdash.db.db_base import Base
from typing import Union


class MetaCache(Base):
    """MetaCache ORM Class."""

    __tablename__ = "meta_cache"
    md5: Union[str, Column] = Column(String(255), primary_key=True)
    synapse_id: Union[str, Column] = Column(String(255))
    content: Union[str, Column] = Column(LONGTEXT)
    num_records: Union[int, Column] = Column(Integer)
    percent_completed_fields: Union[float, Column] = Column(Float)

    def __repr__(self):
        """Get summary."""
        return f"<MetaCache({self.synapse_id}, {self.md5})>"
