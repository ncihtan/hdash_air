"""File Counter."""
import logging
from pathlib import Path
from hdash.synapse.file_type import FileType


class FileCounter:
    """
    File Counter.

    Given a matrix of files from Synapse, count the number of
    files of each type.  For example, count the number of BAM files,
    Image files, etc.
    """

    LEGACY_META_FILE_NAME = "synapse_storage_manifest.csv"
    META_FILE_PREFIX = "synapse_storage_manifest_"

    def __init__(self, synapse_df):
        """Construct new File Counter."""
        self.logger = logging.getLogger("airflow.task")

        # Subset the data into files and folders
        self._file_df = synapse_df[synapse_df.type == "file"]
        self._folder_df = synapse_df[synapse_df.type == "folder"]

        # Bin all the files by type
        self._init_file_types()
        self._identify_archive_folders()
        self._walk_files()

    def get_num_files(self, file_type: FileType):
        """Get number of files for the specified file type."""
        return self.file_type_counter.get(file_type.value, 0)

    def get_total_file_size(self, file_type: FileType):
        """Get the total file Size for the specified file type."""
        return self.file_size_counter.get(file_type.value, 0)

    def _identify_archive_folders(self):
        """
        Identify archive folders.

        This is important because files within archives will be excluded.
        """
        self.archive_folder_set = set()
        for row_tuple in self._folder_df.iterrows():
            row = row_tuple[1]
            name = row["name"]
            synapse_id = row["id"]
            if name.lower() == "archive":
                self.archive_folder_set.add(synapse_id)

    def _walk_files(self):
        """Walk through all files and bin them."""
        file_type_list = []
        for row_tuple in self._file_df.iterrows():
            row = row_tuple[1]
            name = row["name"]
            parent_id = row["parentId"]
            path = Path(name)
            if parent_id in self.archive_folder_set:
                file_type = FileType.EXCLUDE.value
            elif name == self.LEGACY_META_FILE_NAME:
                file_type = FileType.EXCLUDE.value
            elif name.startswith(self.META_FILE_PREFIX):
                file_type = FileType.METADATA.value
            else:
                if path.suffix == ".gz":
                    file_extension = "".join(path.suffixes[0:2])
                else:
                    file_extension = path.suffix
                try:
                    file_type = self.file_type_map[file_extension]
                except KeyError:
                    logging.warning("Unrecognized: %s", file_extension)
                    file_type = FileType.OTHER.value
            file_type_list.append(file_type)

        # Aggregate counts by file type
        self._file_df.insert(0, "file_type", file_type_list)
        groups = self._file_df.groupby("file_type")["file_type"].count()
        self.file_type_counter = groups.to_dict()
        groups = self._file_df.groupby("file_type")["dataFileSizeBytes"].sum()
        self.file_size_counter = groups.to_dict()

    def _init_file_types(self):
        self.file_type_map = {
            ".bam": FileType.BAM.value,
            ".fastq": FileType.FASTQ.value,
            ".fastq.gz": FileType.FASTQ.value,
            ".fq.gz": FileType.FASTQ.value,
            ".fq": FileType.FASTQ.value,
            ".tif": FileType.IMAGE.value,
            ".tiff": FileType.IMAGE.value,
            ".svs": FileType.IMAGE.value,
            ".vsi": FileType.IMAGE.value,
            ".png": FileType.IMAGE.value,
            ".csv": FileType.MATRIX.value,
            ".csv.gz": FileType.MATRIX.value,
            ".tsv": FileType.MATRIX.value,
            ".tsv.gz": FileType.MATRIX.value,
            ".mtx": FileType.MATRIX.value,
            ".txt": FileType.MATRIX.value,
            ".h5ad": FileType.MATRIX.value,
            ".pdf": FileType.OTHER.value,
            ".rnk": FileType.OTHER.value,
            ".json": FileType.OTHER.value,
            ".bcf": FileType.OTHER.value,
            ".bzcfg": FileType.OTHER.value,
            ".log": FileType.OTHER.value,
            ".mzML": FileType.OTHER.value,
            ".zstd": FileType.OTHER.value,
            ".DS_Store": FileType.EXCLUDE.value,
            ".vimrc": FileType.EXCLUDE.value,
            ".Rhistory": FileType.EXCLUDE.value,
        }
