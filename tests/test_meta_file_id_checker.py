"""Test MetaFileIdChecker class."""
import pandas as pd
from hdash.util.meta_file_id_checker import MetaFileIdChecker
from hdash.util.categories import Categories


def test_meta_file_id_checker():
    """Test MetaFileId Checker."""
    categories = Categories()

    data_frame = pd.read_csv("tests/data/demographics_invalid_ids.csv")
    meta_id_checker = MetaFileIdChecker("syn123", categories.DEMOGRAPHICS, data_frame)
    error_list = meta_id_checker.error_list
    assert len(error_list) == 4
    assert error_list[0].startswith("Invalid HTAN Participant ID:  HTA3_001")
    assert error_list[1].startswith("Invalid HTAN Participant ID:  HTA3_800_1")
    assert error_list[2].startswith("Invalid HTAN Participant ID:  nan")
    assert error_list[3].startswith("Invalid HTAN Participant ID:  HTA3_8005, ")

    data_frame = pd.read_csv("tests/data/biospecimens_invalid_ids.csv")
    meta_id_checker = MetaFileIdChecker("syn123", categories.BIOSPECIMEN, data_frame)
    error_list = meta_id_checker.error_list
    assert len(error_list) == 3
    assert error_list[0].startswith("Invalid HTAN Biospecimen ID:  HTA3_8001_001_01")
    assert error_list[1].startswith("Invalid HTAN Biospecimen ID:  HTA_8001_002")
    assert error_list[2].startswith("Invalid Adjacent Biospecimen IDs:  HTA3_8001")

    data_frame = pd.read_csv("tests/data/single_cell_level1_invalid_ids.csv")
    meta_id_checker = MetaFileIdChecker(
        "syn123", categories.SC_RNA_SEQ_LEVEL_1, data_frame
    )
    error_list = meta_id_checker.error_list
    assert len(error_list) == 3
    assert error_list[0].startswith(
        "Invalid HTAN Data File ID:  HTA3_8001_4651918348_222"
    )
    assert error_list[1].startswith("Invalid HTAN Data File ID:  HTA3_8001_0837535366")
    assert error_list[2].startswith("Invalid HTAN Parent Biospecimen ID:  HTA3_8001")
