"""Test Path Util."""

from hdash.util.path_util import PathUtil

# pyright: strict


def test_path_util():
    """Test Path Util."""
    path_util = PathUtil()
    assert path_util.truncate_path("em_level_1/008") == "em_level_1/"
    assert path_util.truncate_path("em_level_1/ohsu/008") == "em_level_1/ohsu/"
    assert path_util.truncate_path("em_level_1") == ""
