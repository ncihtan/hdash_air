"""Validate Orphan Files that are not annotated in the Metadata file."""

import os
from typing import List
from hdash.validator.validation_rule import ValidationRule
from hdash.db.atlas_file import AtlasFile
from hdash.synapse.meta_map import MetaMap
from hdash.util.categories import Categories
from hdash.util.path_util import PathUtil


class ValidateOrphanFiles(ValidationRule):
    """Validate Orphan Files."""

    def __init__(self, atlas_id, file_list: List[AtlasFile], meta_file_map: MetaMap):
        """Construct new Validation Rule."""
        super().__init__(
            "H_ORPHAN_FILES",
            "[Beta] Identify orphaned / unannotated files.",
        )
        self.atlas_id = atlas_id
        self.__identify_orphan_files(file_list, meta_file_map)

    def __identify_orphan_files(
        self, file_list: List[AtlasFile], meta_file_map: MetaMap
    ):
        path_util = PathUtil()
        atlas_file_annotated = {}
        categories = Categories()

        # Initialize all files to be un-annotated
        for atlas_file in file_list:
            key = os.path.join(atlas_file.path, atlas_file.name)
            atlas_file_annotated[key] = False

        # Iterate through all meta categories
        meta_root_map = set()
        category_list = meta_file_map.get_categories()
        for category in category_list:
            # We are only interested in assay-specific meta files
            if (
                category in categories.all_assays
                and category != categories.ACCESSORY_MANIFEST
            ):
                meta_file_list = meta_file_map.get_meta_file_list(category)
                for meta_file in meta_file_list:
                    meta_df = meta_file.data_frame
                    meta_root_map.add(meta_file.atlas_file.path)
                    prefix = path_util.truncate_path(meta_file.atlas_file.path)

                    # If file is listed in the data frame, mark as annotated
                    file_name_list = list(meta_df["Filename"])
                    for file_name in file_name_list:
                        key = prefix + file_name
                        atlas_file_annotated[key] = True

        # Check for un-annotated files
        unannotated_folders = {}
        for atlas_file in file_list:
            key = os.path.join(atlas_file.path, atlas_file.name)
            annotated = atlas_file_annotated[key]
            if not annotated:
                unannotated_folders[atlas_file.path] = (
                    unannotated_folders.get(atlas_file.path, 0) + 1
                )

        # Store Errors at Folder Level
        for path in unannotated_folders.keys():
            file_count = unannotated_folders.get(path)
            msg = f"Folder {path} has {file_count} file(s) that are missing metadata."
            self.add_error_message(msg)
