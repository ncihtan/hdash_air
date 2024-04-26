"""Validation Rule."""

from hdash.validator.validation_rule import ValidationRule
from typing import List
from hdash.db.atlas_file import AtlasFile
from hdash.util.cds_name_checker import CdsFileNameChecker


class ValidateFileNames(ValidationRule):
    """Validate File Names."""

    def __init__(self, atlas_id, file_list: List[AtlasFile]):
        """Construct new Validation Rule."""
        super().__init__(
            "H_FILE_NAMES",
            "File names follow Cancer Data Service (CDS) conventions.",
        )
        self.__validate_file_names(file_list)

    def __validate_file_names(self, file_list: List[AtlasFile]):
        cds_name_checker = CdsFileNameChecker()
        for current_file in file_list:
            file_name = current_file.name
            folder_name = current_file.parent_name
            file_name_valid = cds_name_checker.is_file_name_valid(file_name)
            if not file_name_valid:
                msg = (
                    "In folder: %s, file name: %s contains unsupported characters."
                    % (folder_name, file_name)
                )
                self.add_error_message(msg)
