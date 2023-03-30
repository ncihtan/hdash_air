"""Master Synapse Table Reader."""
from typing import List
from hdash.db.atlas_file import AtlasFile
from hdash.synapse.file_type import FileType
from hdash.synapse.file_type_util import FileTypeUtil


class MasterSynapseReader:
    """
    Read the Master Synapse Table.

    The Master Synapse Table contains all files that have been registered
    with HTAN.  The table includes actual files, metadata files, and folders.

    By default, the reader will:

    - Ignore folders.
    - Ignore files placed in archive folders.
    """

    LEGACY_META_FILE_NAME = "synapse_storage_manifest.csv"

    def __init__(self, atlas_id, synapse_df):
        """Create Reader with Synapse Data Frame."""
        self.atlas_id = atlas_id
        self.synapse_df = synapse_df
        self.file_type_util = FileTypeUtil()

        # Get all archive folders
        archive_df = synapse_df[synapse_df.name.str.lower() == "archive"]
        archive_id_set = set(archive_df.id)

        # Get all files
        file_df = synapse_df[synapse_df.type == "file"]

        # Remove any files in archive folders
        file_df = file_df[~file_df.parentId.isin(archive_id_set)]

        # Fill in NAs
        file_df.Component = file_df.Component.fillna('NA')

        # Convert to File List
        file_list = file_df.apply(self._create_file, axis=1)

        # Remove Excluded Files
        if len(file_list) > 0:
            self.file_list = list(
                filter(lambda x: x.data_type != FileType.EXCLUDE, file_list)
            )
        else:
            self.file_list = file_list

    def get_file_list(self) -> List[AtlasFile]:
        """Get the List of Files."""
        return self.file_list

    def _create_file(self, row):
        file = AtlasFile()
        file.synapse_id = row.id
        file.name = row["name"]
        file.file_type = row.type
        file.parent_id = row.parentId
        file.component = row.Component
        file.size_bytes = row.dataFileSizeBytes
        file.md5 = row.dataFileMD5Hex
        file.atlas_id = self.atlas_id
        file.data_type = self.file_type_util.get_file_type(file.name).value
        return file
