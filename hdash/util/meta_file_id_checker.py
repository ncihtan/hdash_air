"""Check HTAN IDs in a Metadata File."""
import logging
from hdash.util.id_util import IdUtil
from hdash.util.id_checker import IdChecker


class MetaFileIdChecker:
    """Check HTAN IDs in a Metadata File."""

    logger = logging.getLogger("airflow.task")

    def __init__(self, synapse_id, category, data_frame):
        """Init MetaFileIdChecker."""
        self.error_list = []
        self.id_util = IdUtil()
        self.id_checker = IdChecker()

        self.synapse_id = synapse_id
        self.category = category
        self.data_frame = data_frame
        self.valid_primary_id_list = []

        # Validate Primary IDs
        primary_id_col = self.id_util.get_primary_id_column(self.category)
        id_list = self.data_frame[primary_id_col].to_list()
        for current_id in id_list:
            current_id = str(current_id)
            if not self.id_checker.is_valid_htan_id(primary_id_col, current_id):
                msg = f"Invalid {primary_id_col}:  {current_id}"
                msg = self._create_error_msg(msg)
                self.error_list.append(msg)
            else:
                self.valid_primary_id_list.append(current_id)

        # Validate Parent IDs
        parent_id_col = self.id_util.get_parent_id_column(self.category)
        if parent_id_col is not None:
            self.__check_adjacent_or_parent_ids(parent_id_col)

        # Validate Adjacent IDs
        adjacent_id_col = self.id_util.get_adjacent_id_column(self.category)
        if adjacent_id_col is not None:
            self.__check_adjacent_or_parent_ids(adjacent_id_col)

    def __check_adjacent_or_parent_ids(self, id_col):
        id_list = self.data_frame[id_col].to_list()
        if id_col == self.id_util.HTAN_PARENT_ID:
            target_check = self.id_util.HTAN_PARTICIPANT_ID
        else:
            target_check = self.id_util.HTAN_BIOSPECIMEN_ID
        for current_id_list in id_list:
            current_id_list = str(current_id_list)
            current_id_list = current_id_list.replace(";", ",")
            current_id_list = current_id_list.split(",")
            for current_id in current_id_list:
                current_id = current_id.strip()
                if not self.id_checker.is_valid_htan_id(target_check, current_id):
                    error_msg = f"Invalid {id_col}:  {current_id}"
                    msg = self._create_error_msg(error_msg)
                    self.error_list.append(msg)

    def _create_error_msg(self, msg):
        """Create Error Message with Synapse ID."""
        error_msg = f"{msg} [Error occurred while processing file:  "
        error_msg += f"{self.synapse_id} of type {self.category}]."
        return error_msg
