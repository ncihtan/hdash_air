"""Therapy ORM Class."""
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import LONGTEXT
from hdash.db.db_base import Base


class Therapy(Base):
    """Therapy ORM Class."""

    __tablename__ = "therapy"

    atlas_id = Column(String(255), primary_key=True)
    label = Column(String(255))
    content = Column(LONGTEXT)

    def __repr__(self):
        """Get summary."""
        return f"<Therapy({self.label})>"
    
    def get_content(self):
        """Get Content."""
        return self.content
    
    def has_data(self):
        """Get Data Status."""
        return (len(self.content) > 0)
