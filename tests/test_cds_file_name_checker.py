"""Test FileCounter class."""
from hdash.util.cds_name_checker import CdsFileNameChecker


def test_file_name_checker():
    """Test File Name Checker."""
    file_name_checker = CdsFileNameChecker()
    assert file_name_checker.is_file_name_valid("Hello_World-1100.txt")
    assert file_name_checker.is_file_name_valid("hello$.txt") is False
    assert file_name_checker.is_file_name_valid("hello*.txt") is False
