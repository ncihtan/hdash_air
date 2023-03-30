"""Test File Type Utility Class."""
from hdash.synapse.file_type_util import FileTypeUtil
from hdash.synapse.file_type import FileType


def test_file_type_util():
    """Test File Type Utility Class."""
    util = FileTypeUtil()
    assert util.get_file_type("dfci.bam") == FileType.BAM
    assert util.get_file_type("dfci.csv") == FileType.MATRIX
    assert util.get_file_type("dfci.bam.gz") == FileType.BAM
    assert util.get_file_type("dfci.h5ad") == FileType.MATRIX
    assert util.get_file_type("synapse_storage_manifest_assay") == FileType.METADATA
    assert util.get_file_type("synapse_storage_manifest.csv") == FileType.EXCLUDE
    assert util.get_file_type(".DS_Store") == FileType.EXCLUDE
    assert util.get_file_type(".Rhistory") == FileType.EXCLUDE
    assert util.get_file_type(".Other") == FileType.OTHER
