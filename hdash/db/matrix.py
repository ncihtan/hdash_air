"""Matrix ORM Class."""
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.mysql import LONGTEXT
from hdash.db.db_base import Base


class Matrix(Base):
    """Matrix ORM Class."""

    __tablename__ = "matrix"

    matrix_id = Column(Integer, primary_key=True, autoincrement=True)
    atlas_id = Column(String(255))
    order = Column(Integer)
    label = Column(String(255))
    bg_color = Column(String(255))
    content = Column(LONGTEXT)

    def __repr__(self):
        """Get atlas stats summary."""
        return f"<Matrix({self.label})>"
