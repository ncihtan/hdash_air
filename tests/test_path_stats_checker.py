"""Test Path Stats Checker."""
from hdash.stats.path_stats_checker import PathStatsChecker
from hdash.db.atlas_file import AtlasFile
from hdash.util.categories import Categories


def test_path_stats_checker():
    """Test Path Stats Checker."""
    categories = Categories()
    atlas_file_list = [
        __create_atlas_file(
            "sc_rna_seq_level_1/lusc", "sample1.fastq.gz", categories.SC_RNA_SEQ_LEVEL_1
        ),
        __create_atlas_file(
            "sc_rna_seq_level_1/lusc", "sample2.fastq.gz", categories.SC_RNA_SEQ_LEVEL_1
        ),
        __create_atlas_file("sc_rna_seq_level_1/lusc", "sample3.fastq.gz", "NA"),
        __create_atlas_file("sc_rna_seq_level_1/luad", "sample4.fastq.gz", None),
    ]
    root_folder_map = {}
    root_folder_map["sc_rna_seq_level_1"] = {"id": "syn123"}
    path_stats_checker = PathStatsChecker("HTA1", atlas_file_list, root_folder_map)
    path_map = path_stats_checker.path_map

    # We should get back a root sc_rna_seq_level_1
    # with 2 annotated files, 2 unannotated files
    path_stats = path_map["sc_rna_seq_level_1"]
    assert path_stats.num_annotated_files == 2
    assert path_stats.num_un_annotated_files == 2
    assert path_stats.synapse_id == "syn123"


def __create_atlas_file(path, file_name, category):
    atlas_file = AtlasFile()
    atlas_file.path = path
    atlas_file.name = file_name
    atlas_file.category = category
    return atlas_file
