"""File Type."""
from enum import Enum


class FileType(Enum):
    """File Type Enumeration."""

    BAM = "BAM"
    FASTQ = "FASTQ"
    IMAGE = "IMAGE"
    MATRIX = "MATRIX"
    METADATA = "METADATA"
    OTHER = "OTHER_ASSAY"
    EXCLUDE = "EXCLUDE"
