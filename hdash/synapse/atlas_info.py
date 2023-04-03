"""Atlas Info."""
from typing import List
from hdash.db.atlas import Atlas
from hdash.db.validation import Validation
from hdash.db.atlas_stats import AtlasStats
from hdash.db.matrix import Matrix
from hdash.synapse.meta_file import MetaFile


class AtlasInfo:
    """Encapsulate Atlas Info with Stats."""

    def __init__(
        self,
        atlas: Atlas,
        atlas_stats: AtlasStats,
        meta_list: List[MetaFile],
        validation_list: List[Validation],
        matrix_list: List[Matrix],
    ):
        """Create new Atlas Info Object."""
        self.info = atlas
        self.stats = atlas_stats
        self.meta_list = meta_list
        self.validation_list = validation_list
        self.matrix_list = matrix_list

    def get_total_num_errors(self):
        """Get total number of validation errors."""
        num_errors = 0
        for validation in self.validation_list:
            error_list = validation.error_list
            num_errors += len(error_list)
        return num_errors
