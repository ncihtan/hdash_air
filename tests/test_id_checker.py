"""Test IdChecker class."""

from hdash.util.id_util import IdUtil
from hdash.util.id_checker import IdChecker


def test_id_checker():
    """Test ID Validator."""
    id_checker = IdChecker()
    participant_id = IdUtil.HTAN_PARTICIPANT_ID
    biospecimen_id = IdUtil.HTAN_BIOSPECIMEN_ID
    file_id = IdUtil.HTAN_DATA_FILE_ID

    # Check Participant IDs
    assert id_checker.is_valid_htan_id(participant_id, "HTA4_1")
    assert id_checker.is_valid_htan_id(participant_id, "HTA22_122")
    assert id_checker.is_valid_htan_id(participant_id, "HTA6_EXT1")
    assert id_checker.is_valid_htan_id(participant_id, "HTA4_01")

    # Check Derived IDs
    assert id_checker.is_valid_htan_id(biospecimen_id, "HTA4_1_1")
    assert id_checker.is_valid_htan_id(biospecimen_id, "HTA4_0000_1")
    assert id_checker.is_valid_htan_id(biospecimen_id, "HTA6_EXT1_1")
    assert id_checker.is_valid_htan_id(biospecimen_id, "HTA3_8001_1")
    assert id_checker.is_valid_htan_id(file_id, "HTA4_01_1")
    assert id_checker.is_valid_htan_id(file_id, "HTA10_01_002013014")
    assert id_checker.is_valid_htan_id(
        file_id, "HTA10_01_00491395202451674766778335220084"
    )
    assert id_checker.is_valid_htan_id(file_id, "HTA4_1_1_2") is False
