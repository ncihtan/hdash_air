"""Test HTAN Validator class."""
from hdash.validator.htan_validator import HtanValidator
from hdash.graph.graph_creator import GraphCreator
from hdash.db.atlas_file import AtlasFile
from hdash.synapse.meta_map import MetaMap

# pyright: strict


def test_validator(sample_meta_map: MetaMap):
    """Test core HTAN Validator."""
    meta_map = sample_meta_map

    file_list = [
        __create_atlas_file(
            "Linh_UCLA/Case1/"
            + "Ground-glass-opacity/Ground-glass-opacity_S8_L001_R1_001.fastq.gz"
        ),
        __create_atlas_file("orphan1.txt"),
        __create_atlas_file("orphan2.txt"),
    ]
    graph_creator = GraphCreator("HTA3", meta_map)
    htan_graph = graph_creator.htan_graph
    validator = HtanValidator("HTA3", meta_map, htan_graph, file_list)
    validation_list = validator.get_validation_results()

    assert len(validation_list) == 8
    assert validation_list[0].validation_passed()
    assert validation_list[1].validation_passed()
    assert validation_list[2].validation_passed()
    assert validation_list[3].validation_passed()
    assert validation_list[4].validation_passed() is False
    assert len(validation_list[4].error_list) == 2
    error_list = validation_list[4].error_list
    assert error_list[0].error_msg.startswith(
        "Invalid HTAN Data File ID:  HTA3_xxxx_4353967957"
    )

    assert not validation_list[5].validation_passed()
    error_list = validation_list[5].error_list
    assert error_list[0].error_msg.startswith(
        "HTA3_8001_1 references adjacent ID=HTA3_8001_1002"
    )
    assert validation_list[6].validation_passed()
    assert validation_list[7].validation_passed() is False
    error_list = validation_list[7].error_list
    assert error_list[0].error_msg.startswith(
        "In folder: sc_rna_seq_level_1, file name"
    )


def __create_atlas_file(file_name: str):
    atlas_file = AtlasFile()
    atlas_file.name = file_name
    atlas_file.path = "sc_rna_seq_level_1"
    return atlas_file
