"""Validation ORM Class."""
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey
from hdash.db.db_base import Base
from typing import Union


class Validation(Base):
    """Validation ORM Class."""

    __tablename__ = "validation"
    validation_id: Union[int, Column] = Column(
        Integer, primary_key=True, autoincrement=True
    )
    atlas_id: Union[str, Column] = Column(String(255))
    validation_order: Union[int, Column] = Column(Integer)
    validation_code: Union[str, Column] = Column(String(255))
    validation_text: Union[str, Column] = Column(String(255))
    error_list = relationship("ValidationError", backref="validation")

    def __init__(self, atlas_id, validation_code, validation_text):
        """Create new Validation Object."""
        self.atlas_id = atlas_id
        self.validation_code = validation_code
        self.validation_text = validation_text

    def __repr__(self):
        """Get summary."""
        return f"<ValidationResult({self.validation_code})>"

    def validation_passed(self):
        """Determine if the validation passed."""
        return len(self.error_list) == 0


class ValidationError(Base):
    """ValidationError ORM Class."""

    __tablename__ = "validation_error"
    validation_error_id = Column(Integer, primary_key=True, autoincrement=True)
    validation_id = Column(Integer, ForeignKey("validation.validation_id"))
    order: Union[int, Column] = Column(Integer)
    error_msg: Union[str, Column] = Column(String(1000))

    def __repr__(self):
        """Get summary."""
        return f"<ValidationError({self.error_msg})>"
