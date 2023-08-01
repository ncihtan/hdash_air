"""Validation Rule."""

import re
from hdash.util.id_util import IdUtil
from hdash.util.categories import Categories
from hdash.validator.validation_rule import ValidationRule
from hdash.synapse.meta_map import MetaMap
from hdash.synapse.meta_file import MetaFile


class ValidatePrimaryIds(ValidationRule):
    """Validate Primary IDs in all Files."""

    def __init__(self, atlas_id, meta_file_map: MetaMap):
        """Construct new Validation Rule."""
        super().__init__(
            "H_ID_SPEC",
            "Primary IDs follow the HTAN ID Spec.",
        )
        self.primary_id_set = {}

        # List of Files to Exclude from Validation
        self._exclude_list = ["syn42292434"]  # HTAP Ex-Seq Data Set

        self.meta_file_map = meta_file_map
        self.categories = Categories()
        self.id_util = IdUtil()
        for category in self.categories.all_assays:
            self.__validate_ids(atlas_id, category)

    def __validate_ids(self, atlas_id, category):
        if self.meta_file_map.has_category(category):
            meta_file_list = self.meta_file_map.get_meta_file_list(category)
            for meta_file in meta_file_list:
                if meta_file.atlas_file.synapse_id not in self._exclude_list:
                    data_frame = meta_file.data_frame
                    primary_id_col = self.id_util.get_primary_id_column(category)
                    id_list = data_frame[primary_id_col].to_list()
                    for current_id in id_list:
                        current_id = str(current_id)
                        if primary_id_col == IdUtil.HTAN_PARTICIPANT_ID:
                            self.__check_participant_id(
                                meta_file, category, current_id, atlas_id
                            )
                        else:
                            self.__check_primary_id(
                                meta_file, category, current_id, atlas_id
                            )

    def __check_participant_id(
        self, meta_file: MetaFile, category, participant_id, atlas_id
    ):
        parts = participant_id.split("_")
        label = category + ": " + participant_id
        if parts[0] != atlas_id:
            msg = label + " does not match atlas ID: " + atlas_id
            self.add_error(msg, meta_file)
        if len(parts) != 2:
            msg = label + " does not match HTAN spec."
            self.add_error(msg, meta_file)
        else:
            try:
                int(parts[1])
            except ValueError:
                msg = label + " does not match HTAN spec."
                self.add_error(msg, meta_file)

    def __check_primary_id(self, meta_file: MetaFile, category, primary_id, atlas_id):
        primary_id = str(primary_id)
        if "," in primary_id:
            msg = "Primary ID can only have one ID:  " + primary_id
            self.add_error(msg, meta_file)
        elif primary_id == "nan":
            msg = "Primary ID is missing from specific row."
            self.add_error(msg, meta_file)
        elif primary_id in self.primary_id_set:
            msg = f"Primary ID {primary_id} has already been defined in {category}."
            self.add_error(msg, meta_file)
        else:
            match = bool(re.match(
                "^(HTA([1-9]|1[0-5]))_((EXT)?([0-9]\d*|0000))_([0-9]\d*|0000)$",
                primary_id)
            )
            if not match:
                msg = primary_id + " does not match HTAN spec."
                self.add_error(msg, meta_file)
