"""Check HTAN IDs against SOP."""
import re
from hdash.util.id_util import IdUtil


class IdChecker:
    """ID Checker Class."""

    PARTICIPANT_ID = r"^(HTA([1-9]|[1-9]\d))_((EXT)?(\d*|0000))$"
    DERIVED_ID = r"^(HTA([1-9]|[1-9]\d))_((EXT)?(\d*|0000))_(\d*|0000)$"

    def __init__(self):
        """Init IdChecker."""
        self.participant_regex = re.compile(IdChecker.PARTICIPANT_ID)
        self.derived_regex = re.compile(IdChecker.DERIVED_ID)

    def is_valid_htan_id(self, id_type: str, htan_id: str):
        """Determine if HTAN ID is valid."""
        if id_type == IdUtil.HTAN_PARTICIPANT_ID:
            return self.participant_regex.match(htan_id) is not None
        return self.derived_regex.match(htan_id) is not None
