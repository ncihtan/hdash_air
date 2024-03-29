"""Matrix ORM Class."""
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.mysql import LONGTEXT
from hdash.db.db_base import Base


class Matrix(Base):
    """Matrix ORM Class."""

    __tablename__ = "matrix"

    matrix_id = Column(String(255), primary_key=True)
    atlas_id = Column(String(255))
    order = Column(Integer)
    label = Column(String(255))
    content = Column(LONGTEXT)

    def __repr__(self):
        """Get summary."""
        return f"<Matrix({self.label})>"
