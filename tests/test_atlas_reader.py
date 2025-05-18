"""Test Atlas Reader."""
from hdash.reader.atlas_reader import AtlasReader

# pyright: strict

def test_atlas_reader():
    """Test Atlas Reader."""
    reader = AtlasReader("tests/data/htan_projects.csv")
    assert len(reader.atlas_list) == 15
    atlas0 = reader.atlas_list[0]
    assert atlas0.atlas_id == "HTA1"
    assert atlas0.name == "PILOT - HTAPP"
