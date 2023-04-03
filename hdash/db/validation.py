"""Validation ORM Class."""
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey
from hdash.db.db_base import Base


class Validation(Base):
    """Validation ORM Class."""

    __tablename__ = "validation"
    validation_id = Column(Integer, primary_key=True, autoincrement=True)
    atlas_id = Column(String(255))
    validation_order = Column(Integer, autoincrement=True)
    validation_code = Column(String(255))
    validation_text = Column(String(255))
    error_list = relationship("ValidationError", backref="validation")

    def __init__(self, atlas_id, validation_code, validation_text):
        """Create new Validation Object."""
        self.atlas_id = atlas_id
        self.validation_code = validation_code
        self.validation_text = validation_text

    def __repr__(self):
        """Get atlas file summary."""
        return f"<ValidationResult({self.validation_code})>"

    def validation_passed(self):
        """Determine if the validation passed."""
        return len(self.error_list) == 0


class ValidationError(Base):
    """ValidationError ORM Class."""

    __tablename__ = "validation_error"
    validation_error_id = Column(Integer, primary_key=True, autoincrement=True)
    validation_id = Column(Integer, ForeignKey("validation.validation_id"))
    order = Column(Integer, autoincrement=True)
    error_msg = Column(String(1000))

    def __repr__(self):
        """Get atlas file summary."""
        return f"<ValidationError({self.error_msg})>"
