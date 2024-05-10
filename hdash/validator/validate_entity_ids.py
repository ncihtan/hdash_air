"""Validation Rule."""
from hdash.util.categories import Categories
from hdash.validator.validation_rule import ValidationRule
from hdash.synapse.meta_map import MetaMap
from hdash.synapse.meta_file import MetaFile


class ValidateEntityIds(ValidationRule):
    """Verify that Entity Ids are Specified."""

    def __init__(self, meta_file_map: MetaMap):
        """Construct new Validation Rule."""
        categories = Categories()
        super().__init__("H_ENTITY_ID", "Synapse Entity IDs are Specified for Assays.")
        category_list = meta_file_map.get_categories()
        for category in category_list:
            # Check for Entity IDs in All Assays.
            # Exclude biospecimen and clinical metadata from validation checks.
            if (
                category in categories.all_assays
                and category != categories.ACCESSORY_MANIFEST
            ):
                meta_file_list = meta_file_map.get_meta_file_list(category)
                for meta_file in meta_file_list:
                    data_frame = meta_file.data_frame
                    try:
                        synapse_ids = data_frame[Categories.ENTITY_ID_COL].to_list()
                        self.__check_synapse_ids(meta_file, category, synapse_ids)
                    except KeyError:
                        error_msg = (
                            f"{category} does not have "
                            f"{Categories.ENTITY_ID_COL} column."
                        )
                        self.add_error(error_msg, meta_file)

    def __check_synapse_ids(self, meta_file: MetaFile, category, synapse_ids):
        for synapse_id in synapse_ids:
            if not str(synapse_id).startswith("syn"):
                error_msg = f"{category} has invalid Synapse ID: {synapse_id}."
                self.add_error(error_msg, meta_file)
