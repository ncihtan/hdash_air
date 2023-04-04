"""MetaCache ORM Class."""
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.dialects.mysql import LONGTEXT
from hdash.db.db_base import Base


class MetaCache(Base):
    """MetaCache ORM Class."""

    __tablename__ = "meta_cache"
    synapse_id = Column(String(255), primary_key=True)
    md5 = Column(String(255))
    content = Column(LONGTEXT)
    num_records = Column(Integer)
    percent_completed_fields = Column(Float)

    def __repr__(self):
        """Get summary."""
        return f"<MetaCache({self.synapse_id}, {self.md5})>"
