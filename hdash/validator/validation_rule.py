"""Base Validation Rule."""

from hdash.synapse.meta_file import MetaFile


class ValidationRule:
    """Base Validation Rule."""

    def __init__(self, validation_code: str, validation_text: str):
        """Construct Base Validation Rule."""
        self.validation_code = validation_code
        self.validation_text = validation_text
        self.error_list: list[str] = []

    def validation_passed(self):
        """Determine if the validation passed."""
        return len(self.error_list) == 0

    def add_error(self, msg: str, meta_file: MetaFile):
        """Add Validation Error."""
        msg = self._create_error_msg(msg, meta_file)
        self.error_list.append(msg)

    def add_error_message(self, msg: str):
        """Add Validation Error."""
        self.error_list.append(msg)

    def _create_error_msg(self, msg: str, meta_file: MetaFile):
        """Create Error Message with Synapse ID."""
        synapse_id = meta_file.atlas_file.synapse_id
        category = meta_file.atlas_file.category
        error_msg = f"{msg} [Error occurred while processing file:  "
        error_msg += f"{synapse_id} of type {category}]."
        return error_msg
