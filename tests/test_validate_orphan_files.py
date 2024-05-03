"""Test Validate Orphan Files"""
from hdash.util.categories import Categories
from hdash.validator.validate_orphan_files import ValidateOrphanFiles
from hdash.db.atlas_file import AtlasFile


def test_orphan_validator(sample_meta_map):
    """Test Orphan Validator"""
    meta_map = sample_meta_map

    path1 = "sc_rna_seq_level_1/Linh_UCLA/Case1/Ground-glass-opacity/"
    path2 = "sc_rna_seq_level_1/OHSU"
    file_list = [
        __create_atlas_file(path1, "Ground-glass-opacity_S8_L001_R1_001.fastq.gz"),
        __create_atlas_file(path1, "orphan1.txt"),
        __create_atlas_file(path2, "orphan2.txt"),
    ]

    meta_file_list = sample_meta_map.get_meta_file_list(Categories.SC_RNA_SEQ_LEVEL_1)
    meta_file_list[0].atlas_file.path = "sc_rna_seq_level_1"

    validate_orphan_files = ValidateOrphanFiles("HTA1", file_list, meta_map)
    error_list = validate_orphan_files.error_list
    assert len(error_list) == 2

    assert error_list[0].startswith(
        "Folder sc_rna_seq_level_1/Linh_UCLA/Case1/Ground-glass-opacity/ has 1 "
        + "file(s) that"
    )
    assert error_list[1].startswith("Folder sc_rna_seq_level_1/OHSU has 1 file(s) that")


def __create_atlas_file(path, file_name):
    atlas_file = AtlasFile()
    atlas_file.path = path
    atlas_file.name = file_name
    return atlas_file
