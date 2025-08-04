"""Matrix ORM Class."""

from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.mysql import LONGTEXT
from hdash.db.db_base import Base
from typing import Union


class Matrix(Base):
    """Matrix ORM Class."""

    __tablename__ = "matrix"

    matrix_id: Union[str, Column] = Column(String(255), primary_key=True)
    atlas_id: Union[str, Column] = Column(String(255))
    order: Union[int, Column] = Column(Integer)
    label: Union[str, Column] = Column(String(255))
    content: Union[str, Column] = Column(LONGTEXT)

    def __repr__(self):
        """Get summary."""
        return f"<Matrix({self.label})>"
