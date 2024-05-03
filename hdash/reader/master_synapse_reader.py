"""Master Synapse Table Reader."""
from typing import List
from hdash.db.atlas_file import AtlasFile
from hdash.synapse.file_type import FileType
from hdash.synapse.file_type_util import FileTypeUtil
import math


class MasterSynapseReader:
    """
    Read the Master Synapse Table.

    The Master Synapse Table contains all files that have been registered
    with HTAN.  The table includes actual files, metadata files, and folders.
    """

    def __init__(self, atlas_id, synapse_df):
        """Create Reader with Synapse Data Frame."""
        self.atlas_id = atlas_id
        self.synapse_df = synapse_df
        self.file_type_util = FileTypeUtil()

        # Get all folders
        folder_df = synapse_df[synapse_df.type == "folder"]
        folder_map = folder_df.set_index("id").to_dict("index")

        # Get all files
        file_df = synapse_df[synapse_df.type == "file"]

        # Fill in NAs
        file_df.Component = file_df.Component.fillna("NA")

        # Convert to File List
        file_list = file_df.apply(self._create_file, axis=1, args=(folder_map,))

        if len(file_list) > 0:
            # Remove Excluded Files
            file_list = list(
                filter(lambda x: x.data_type != FileType.EXCLUDE.value, file_list)
            )

            # Remove any archived files
            file_list = list(
                filter(lambda x: not x.path.startswith("archive"), file_list)
            )

            # Bin Files into meta v. non-meta and filter meta files by most recent
            meta_files = list(
                filter(lambda x: x.data_type == FileType.METADATA.value, file_list)
            )
            non_meta_files = list(
                filter(lambda x: x.data_type != FileType.METADATA.value, file_list)
            )
            meta_files = self.filter_meta_files_by_most_recent(meta_files)

            # Merge back together
            self.file_list = []
            self.file_list.extend(meta_files)
            self.file_list.extend(non_meta_files)
        else:
            self.file_list = []

    def filter_meta_files_by_most_recent(self, meta_files):
        """If a folder has more than one meta file, keep the most recent one."""
        folder_map = {}
        for file in meta_files:
            if file.parent_id in folder_map:
                stored_file = folder_map[file.parent_id]
                if file.modified_on > stored_file.modified_on:
                    folder_map[file.parent_id] = file
            else:
                folder_map[file.parent_id] = file
        return list(folder_map.values())

    def get_file_list(self) -> List[AtlasFile]:
        """Get the List of Files."""
        return self.file_list

    def _create_file(self, row, folder_map):
        file = AtlasFile()
        file.synapse_id = row.id
        file.name = row["name"]
        file.file_type = row.type
        file.parent_id = row.parentId
        file.path = self._get_path(row, folder_map)
        file.category = row.Component
        file.size_bytes = row.dataFileSizeBytes
        # Check edge case of empty size
        if math.isnan(file.size_bytes):
            file.size_bytes = 0
        file.md5 = str(row.dataFileMD5Hex)
        file.modified_on = row.modifiedOn
        file.atlas_id = self.atlas_id
        file.data_type = self.file_type_util.get_file_type(file.name)
        return file

    def _get_path(self, row, folder_map):
        """This method will walk up the tree to get the full path."""
        path = ""
        parent_id = row.parentId

        while parent_id is not None and parent_id in folder_map:
            parent_row = folder_map[parent_id]
            parent_name = parent_row["name"]
            if len(path) > 0:
                path = parent_name + "/" + path
            else:
                path = parent_name
            parent_id = parent_row["parentId"]
        return path
