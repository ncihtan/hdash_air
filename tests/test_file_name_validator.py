"""Test FileCounter class."""
from hdash.validator.validate_file_names import ValidateFileNames
from hdash.db.atlas_file import AtlasFile


def test_file_name_checker():
    """Test File Name Validator."""
    file_list = [
        __create_atlas_file("Hello_World-1100.txt"),
        __create_atlas_file("hello$.txt"),
        __create_atlas_file("hello*.txt"),
    ]
    validator = ValidateFileNames("HTA1", file_list)
    error_list = validator.error_list
    assert len(error_list) == 2
    assert error_list[0].startswith("In folder: root, file name: hello$.txt contains")
    assert error_list[1].startswith("In folder: root, file name: hello*.txt")


def __create_atlas_file(file_name):
    atlas_file = AtlasFile()
    atlas_file.name = file_name
    atlas_file.parent_name = "root"
    return atlas_file
