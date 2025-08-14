"""h5ad ORM Class."""

from sqlalchemy import Column, String, Boolean, DateTime, func
from sqlalchemy.dialects.mysql import LONGTEXT
from hdash.db.db_base import Base
from typing import Union
from datetime import datetime


class H5adValidation(Base):
    """h5ad ORM Class."""

    __tablename__ = "h5ad_validation"
    bucket: Union[str, Column] = Column(String(32), primary_key=True)
    key: Union[str, Column] = Column(String(900), primary_key=True)
    valid: Union[bool, Column] = Column(Boolean)
    error_list: Union[str, Column] = Column(LONGTEXT)
    created_at: Union[datetime, Column] = Column(DateTime, default=func.now())

    def __init__(self):
        """Create h5ad validation record."""
        self.valid = False

    def __repr__(self):
        """Get summary."""
        return f"<H5ad Validation({self.bucket}, {self.key})>"
