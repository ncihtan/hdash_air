"""Validation Rule."""

from hdash.util.id_util import IdUtil
from hdash.util.categories import Categories
from hdash.validator.validation_rule import ValidationRule
from hdash.synapse.meta_map import MetaMap
from hdash.synapse.meta_file import MetaFile
from hdash.util.meta_file_id_checker import MetaFileIdChecker


class ValidateHtanIds(ValidationRule):
    """Validate Primary IDs in all Files."""

    def __init__(self, atlas_id, meta_file_map: MetaMap):
        """Construct new Validation Rule."""
        super().__init__(
            "H_ID_SPEC",
            "HTAN IDs follow the SOP.",
        )
        self.primary_id_set = {}
        self.atlas_id = atlas_id

        # List of Files to Exclude from Validation
        self._exclude_list = ["syn42292434"]  # HTAP Ex-Seq Data Set

        self.meta_file_map = meta_file_map
        self.categories = Categories()
        self.id_util = IdUtil()
        for category in self.categories.all_assays:
            self.__validate_ids(category)

    def __validate_ids(self, category):
        if self.meta_file_map.has_category(category):
            meta_file_list = self.meta_file_map.get_meta_file_list(category)
            for meta_file in meta_file_list:
                if meta_file.atlas_file.synapse_id not in self._exclude_list:
                    meta_id_checker = MetaFileIdChecker(
                        meta_file.atlas_file.synapse_id,
                        meta_file.atlas_file.category,
                        meta_file.data_frame,
                    )
                    self.error_list.extend(meta_id_checker.error_list)
                    self.__check_unique_primary_ids(
                        meta_file, category, meta_id_checker.valid_primary_id_list
                    )

    def __check_unique_primary_ids(
        self, meta_file: MetaFile, category, primary_id_list
    ):
        for primary_id in primary_id_list:
            if primary_id in self.primary_id_set:
                (defined_synapse_id, defined_category) = self.primary_id_set[primary_id]
                msg = (
                    f"Primary ID {primary_id} has already been defined in file "
                    f"{defined_synapse_id} of type {defined_category}."
                )
                self.add_error(msg, meta_file)
            else:
                synapse_id = meta_file.atlas_file.synapse_id
                self.primary_id_set[primary_id] = (synapse_id, category)
