"""PyTest Fixtures."""
from typing import List
import pytest
from hdash.util.categories import Categories
from hdash.db.atlas import Atlas
from hdash.db.atlas_file import AtlasFile
from hdash.db.meta_cache import MetaCache
from hdash.synapse.meta_file import MetaFile
from hdash.synapse.meta_map import MetaMap


@pytest.fixture
def init_atlas_list():
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


def _init_atlas_list() -> List[Atlas]:
    atlas_list: List[Atlas] = [
        _create_atlas("syn23448901", "HTA1", "HTAN MSKCC"),
        _create_atlas("syn22093319", "HTA2", "HTAN OHSU"),
        _create_atlas(
            "syn21050481",
            "HTA3",
            "HTAN Vanderbilt",
            "Vesteinn",
        ),
    ]
    return atlas_list


def _create_atlas(synapse_id, atlas_id, name, liaison=None):
    atlas = Atlas(atlas_id, name, synapse_id, liaison)
    return atlas
