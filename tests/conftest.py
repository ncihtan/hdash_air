"""PyTest Fixtures."""
from typing import List
import pytest

from hdash.synapse.file_type import FileType
from hdash.util.categories import Categories
from hdash.db.atlas import Atlas
from hdash.db.atlas_file import AtlasFile
from hdash.db.atlas_stats import AtlasStats
from hdash.db.validation import Validation, ValidationError
from hdash.synapse.atlas_info import AtlasInfo
from hdash.db.meta_cache import MetaCache
from hdash.db.matrix import Matrix
from hdash.synapse.meta_file import MetaFile
from hdash.synapse.meta_map import MetaMap


@pytest.fixture
def atlas_list():
    """Init project list."""
    return _init_atlas_list()


@pytest.fixture
def sample_meta_map():
    """Get Sample Meta Map Object."""
    categories = Categories()
    record_list = [
        ("tests/data/demographics.csv", categories.DEMOGRAPHICS),
        ("tests/data/biospecimens.csv", categories.BIOSPECIMEN),
        ("tests/data/single_cell_level1.csv", categories.SC_RNA_SEQ_LEVEL_1),
        ("tests/data/single_cell_level2.csv", categories.SC_RNA_SEQ_LEVEL_2),
        ("tests/data/single_cell_level3.csv", categories.SC_RNA_SEQ_LEVEL_3),
        ("tests/data/single_cell_level4.csv", categories.SC_RNA_SEQ_LEVEL_4),
    ]
    meta_file_list = _create_meta_file_list(record_list)

    meta_map = MetaMap()
    for meta_file in meta_file_list:
        meta_map.add_meta_file(meta_file)
    return meta_map


def _create_meta_file_list(record_list) -> List[MetaFile]:
    meta_file_list: List[MetaFile] = []
    synapse_id = 1
    for record in record_list:
        path = record[0]
        category = record[1]
        atlas_file = AtlasFile()
        atlas_file.name = path
        atlas_file.category = category
        atlas_file.synapse_id = f"synapse_{synapse_id}"

        meta_cache = MetaCache()
        meta_cache.synapse_id = atlas_file.synapse_id

        with open(path, "r", encoding="utf-8") as file:
            csv_data = file.read()
            meta_cache.content = csv_data

        meta_file = MetaFile(atlas_file, meta_cache)
        meta_file_list.append(meta_file)
        synapse_id += 1
    return meta_file_list


def _init_atlas_list() -> List[AtlasInfo]:
    local_atlas_list: List[AtlasInfo] = []
    atlas1 = _create_atlas("syn23448901", "HTA1", "HTAN MSKCC", "Ino")

    stats1 = AtlasStats("HTA1")
    stats1.num_matrix_files = 10
    stats1.num_bam_files = 20
    stats1.num_other_files = 30
    stats1.total_file_size = 243294032
    stats1.percent_metadata_complete = 0.55

    validation_list: List[Validation] = []
    validation1 = Validation("HTA1", "H_LINKS", "Check internal links")

    error_list: List[ValidationError] = []
    error1 = ValidationError()
    error1.error_msg = "Invalid ID: XXXX"
    error_list.append(error1)
    validation1.error_list = error_list
    validation_list.append(validation1)

    meta_list: List[MetaFile] = []
    atlas_file1 = AtlasFile()
    atlas_file1.data_type = FileType.METADATA
    atlas_file1.category = Categories.DEMOGRAPHICS
    meta_cache1 = MetaCache()
    meta_cache1.synapse_id = "syn_423421"
    meta_cache1.num_records = 25
    meta_cache1.percent_completed_fields = 0.44
    meta_file1 = MetaFile(atlas_file1, meta_cache1)
    meta_list.append(meta_file1)

    matrix_list = []
    matrix = Matrix()
    matrix.atlas_id = "HTA1"
    matrix.bg_color = "pink"
    matrix.label = "Clinical Data Matrix: Tiers 1 and 2"

    atlas_info1 = AtlasInfo(atlas1, stats1, meta_list, validation_list, matrix_list)
    local_atlas_list.append(atlas_info1)
    return local_atlas_list


def _create_atlas(synapse_id, atlas_id, name, liaison):
    atlas = Atlas(atlas_id, name, synapse_id, liaison)
    return atlas
