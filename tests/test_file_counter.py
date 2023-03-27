"""Test FileCounter class."""
from hdash.db.atlas_file import AtlasFile
from hdash.synapse.file_counter import FileCounter
from hdash.synapse.file_type import FileType
from hdash.synapse.file_type_util import FileTypeUtil


def test_file_counter():
    """Test File Counter."""
    file1 = _create_file("a1", "hta1.bam", 100, "file", "b1")
    file2 = _create_file("a2", "hta1.fq", 100, "file", "b2")
    file3 = _create_file("a3", "hta.tif", 100, "file", "b3")
    file4 = _create_file("a4", "hta2.bam", 100, "file", "b4")

    file_list = [file1, file2, file3, file4]
    counter = FileCounter(file_list)

    assert counter.get_total_file_size() == 400
    assert counter.get_num_files(FileType.BAM) == 2
    assert counter.get_num_files(FileType.IMAGE) == 1
    assert counter.get_num_files(FileType.FASTQ) == 1


def _create_file(synapse_id, file_name, file_size, file_type, parent_id):
    """Create Atlas File."""
    util = FileTypeUtil()
    file = AtlasFile()
    file.synapse_id = synapse_id
    file.name = file_name
    file.size_bytes = file_size
    file.type = file_type
    file.parent_id = parent_id
    file.data_type = util.get_file_type(file_name)
    return file
