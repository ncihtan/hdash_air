"""File Type Utility Class."""
import logging
from pathlib import Path
from hdash.synapse.file_type import FileType


class FileTypeUtil:
    """File Type Utility Class."""
    logger = logging.getLogger("hdash")
    invalid_file_type_set = set()

    LEGACY_META_FILE_NAME = "synapse_storage_manifest.csv"
    META_FILE_PREFIX = "synapse_storage_manifest_"

    def __init__(self):
        """Create FileType Utility."""
        self._init_file_types()

    def get_file_type(self, file_name: str):
        """Determine the file type from the file name."""
        path = Path(file_name)
        file_type = FileType.OTHER
        if file_name == self.LEGACY_META_FILE_NAME:
            file_type = FileType.EXCLUDE
        elif file_name.startswith(self.META_FILE_PREFIX):
            file_type = FileType.METADATA
        else:
            file_extension = self._get_file_extension(path)
            try:
                file_type = self.file_type_map[file_extension]
            except KeyError:
                self.invalid_file_type_set.add(file_extension)
        return file_type.value

    def _get_file_extension(self, path):
        """Get File Extension, remove .gz, as needed."""
        if path.name.startswith("."):
            return path.name
        if path.suffix == ".gz":
            file_extension = "".join(path.suffixes[-2])
        else:
            file_extension = path.suffix
        return file_extension

    def _init_file_types(self):
        """Initialize File Types."""
        self.file_type_map = {
            ".bam": FileType.BAM,
            ".fastq": FileType.FASTQ,
            ".fasta": FileType.FASTQ,
            ".fq": FileType.FASTQ,
            ".tif": FileType.IMAGE,
            ".tiff": FileType.IMAGE,
            ".svs": FileType.IMAGE,
            ".vsi": FileType.IMAGE,
            ".png": FileType.IMAGE,
            ".raw": FileType.IMAGE,
            ".jpg": FileType.IMAGE,
            ".scn": FileType.IMAGE,
            ".s0001_e00": FileType.IMAGE,
            ".csv": FileType.MATRIX,
            ".tsv": FileType.MATRIX,
            ".vcf": FileType.MATRIX,
            ".fcs": FileType.MATRIX,
            ".mtx": FileType.MATRIX,
            ".txt": FileType.MATRIX,
            ".h5ad": FileType.MATRIX,
            ".h5": FileType.MATRIX,
            ".xlsx": FileType.MATRIX,
            ".pdf": FileType.OTHER,
            ".rnk": FileType.OTHER,
            ".json": FileType.OTHER,
            ".bcf": FileType.OTHER,
            ".bzcfg": FileType.OTHER,
            ".log": FileType.OTHER,
            ".mzML": FileType.OTHER,
            ".zstd": FileType.OTHER,
            ".DS_Store": FileType.EXCLUDE,
            ".vimrc": FileType.EXCLUDE,
            ".Rhistory": FileType.EXCLUDE,
        }
