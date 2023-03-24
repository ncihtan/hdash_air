"""AtlasStats ORM Class."""
from sqlalchemy import Column, String, Integer, Float
from hdash.db.db_base import Base


class AtlasStats(Base):
    """AtlasStats ORM Class."""

    __tablename__ = "atlas_stats"

    atlas_id = Column(String(25), primary_key=True)
    total_file_size = Column(Integer)
    num_fastq_files = Column(Integer)
    num_bam_files = Column(Integer)
    num_image_files = Column(Integer)
    num_matrix_files = Column(Integer)
    num_other_files = Column(Integer)
    num_errors = Column(Integer)
    percent_metadata_complete = Column(Float)

    def __init__(self, atlas_id):
        """Create AtlasStats Object."""
        self.atlas_id = atlas_id

    def __repr__(self):
        """Get atlas stats summary."""
        return f"<AtlasStats({self.atlas_id})>"
