"""Atlas Info."""
from hdash.db.atlas import Atlas
from hdash.db.validation import Validation
from hdash.db.atlas_stats import AtlasStats
from hdash.db.path_stats import PathStats
from hdash.db.longitudinal import Longitudinal
from hdash.util.html_matrix import HtmlMatrix
from hdash.synapse.meta_file import MetaFile


class AtlasInfo:
    """Encapsulate Atlas Info with Stats."""

    def __init__(
        self,
        atlas: Atlas,
        atlas_stats: AtlasStats,
        meta_list: list[MetaFile],
        validation_list: list[Validation],
        html_matrix_list: list[HtmlMatrix],
        path_stats_list: list[PathStats],
        longitudinal_table: list[Longitudinal],
    ):
        """Create new Atlas Info Object."""
        self.info = atlas
        self.stats = atlas_stats
        self.meta_list = meta_list
        self.validation_list = validation_list
        self.html_matrix_list = html_matrix_list
        self.path_stats_list = path_stats_list
        self.longitudinal_table = longitudinal_table
        self._calculate_total_num_errors()

    def _calculate_total_num_errors(self):
        """Calculate total number of validation errors."""
        self.num_errors = 0
        for validation in self.validation_list:
            error_list = validation.error_list
            self.num_errors += len(error_list)
