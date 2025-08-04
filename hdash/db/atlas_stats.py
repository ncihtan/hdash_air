"""AtlasStats ORM Class."""

from sqlalchemy import Column, String, Integer, BigInteger, Float
import humanize
from hdash.db.db_base import Base
from typing import Union


class AtlasStats(Base):
    """AtlasStats ORM Class."""

    __tablename__ = "atlas_stats"

    atlas_id: Union[str, Column] = Column(String(25), primary_key=True)
    total_file_size: Union[int, Column] = Column(BigInteger)
    num_fastq_files: Union[int, Column] = Column(Integer)
    num_bam_files: Union[int, Column] = Column(Integer)
    num_image_files: Union[int, Column] = Column(Integer)
    num_matrix_files: Union[int, Column] = Column(Integer)
    num_other_files: Union[int, Column] = Column(Integer)
    percent_metadata_complete: Union[float, Column] = Column(Float)

    def __init__(self, atlas_id):
        """Create AtlasStats Object."""
        self.atlas_id = atlas_id
        self.total_file_size = 0
        self.num_fastq_files = 0
        self.num_bam_files = 0
        self.num_image_files = 0
        self.num_matrix_files = 0
        self.num_other_files = 0
        self.percent_metadata_complete = 0

    def get_total_fize_size_human_readable(self):
        """Get total file size in human readable format, e.g. MB, TB."""
        return humanize.naturalsize(self.total_file_size)  # type: ignore

    def get_total_num_files(self):
        """Get total number of files."""
        return (
            self.num_fastq_files
            + self.num_bam_files
            + self.num_image_files
            + self.num_matrix_files
            + self.num_other_files
        )

    def __repr__(self):
        """Get summary."""
        return f"<AtlasStats({self.atlas_id})>"
