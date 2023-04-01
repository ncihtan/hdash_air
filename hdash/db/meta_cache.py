"""MetaCache ORM Class."""
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import LONGTEXT
from hdash.db.db_base import Base


class MetaCache(Base):
    """MetaCache ORM Class."""

    __tablename__ = "meta_cache"
    synapse_id = Column(String(255), primary_key=True)
    md5 = Column(String(255))
    content = Column(LONGTEXT)

    def __repr__(self):
        """Get atlas file summary."""
        return f"<MetaCache({self.synapse_id}, {self.md5})>"
