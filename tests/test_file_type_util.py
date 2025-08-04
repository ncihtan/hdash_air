"""Test File Type Utility Class."""

from hdash.synapse.file_type_util import FileTypeUtil
from hdash.synapse.file_type import FileType

# pyright: strict


def test_file_type_util():
    """Test File Type Utility Class."""
    util = FileTypeUtil()
    assert util.get_file_type("dfci.bam") == FileType.BAM.value
    assert util.get_file_type("dfci.csv") == FileType.MATRIX.value
    assert util.get_file_type("dfci.bam.gz") == FileType.BAM.value
    assert util.get_file_type("dfci.h5ad") == FileType.MATRIX.value
    assert (
        util.get_file_type("synapse_storage_manifest_assay") == FileType.METADATA.value
    )
    assert util.get_file_type("synapse_storage_manifest.csv") == FileType.EXCLUDE.value
    assert util.get_file_type(".DS_Store") == FileType.EXCLUDE.value
    assert util.get_file_type(".Rhistory") == FileType.EXCLUDE.value
    assert util.get_file_type(".Other") == FileType.OTHER.value
