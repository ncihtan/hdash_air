"""File Counter."""
from collections import Counter
import numpy
from hdash.db.atlas_file import AtlasFile


class FileCounter:
    """
    File Counter.

    Given a list of Atlas Files, count the number of
    files of each type.  For example, count the number of BAM files,
    Image files, etc.
    """

    def __init__(self, file_list: list[AtlasFile]):
        """Construct new File Counter."""
        data_type_list = list(map(lambda file: file.data_type, file_list))
        size_list = list(map(lambda file: file.size_bytes, file_list))

        # Use numpy.nansum just in case we have empty files with NaN sizes
        self.total_file_size = numpy.nansum(size_list)  # type: ignore
        self.counter = Counter(data_type_list)

    def get_num_files(self, file_type: str):
        """Get number of files for the specified file type."""
        return self.counter.get(file_type, 0)

    def get_total_file_size(self):
        """Get the total file size of all files."""
        return self.total_file_size
