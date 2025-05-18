"""Path Stats."""
import os
import logging
from typing import List
from typing import Dict
from hdash.db.atlas_file import AtlasFile
from hdash.db.path_stats import PathStats
from hdash.synapse.file_type import FileType


class PathStatsChecker:
    """Path Stats Checker."""

    logger = logging.getLogger("airflow.task")

    def __init__(self, atlas_id, file_list: List[AtlasFile], root_folder_map):
        """Create PathStats Object."""
        self.logger.info("Performing Path Stats Checker on %d files" % len(file_list))
        self.path_map: Dict[str, PathStats] = {}
        counter = 0

        non_meta_files: List[AtlasFile] = list(
            filter(lambda x: x.data_type != FileType.METADATA.value, file_list)
        )

        for atlas_file in non_meta_files:
            counter += 1
            root_path = atlas_file.path.split(os.sep)[0]
            path_stats = self._get_path_stats(
                root_path, atlas_id, self.path_map, root_folder_map
            )
            if atlas_file.category is None or atlas_file.category == "NA":
                path_stats.num_un_annotated_files += 1  # type: ignore
            else:
                path_stats.num_annotated_files += 1  # type: ignore
        self.logger.info("Path Stats Checker done on %d files" % counter)

    def _get_path_stats(
        self, root_path, atlas_id, path_map: Dict[str, PathStats], root_folder_map
    ):
        if root_path in path_map:
            return path_map[root_path]
        else:
            synapse_id = "NA"
            if root_path in root_folder_map:
                synapse_id = root_folder_map[root_path]["id"]
            path_stats = PathStats(atlas_id, synapse_id, root_path)
            path_map[root_path] = path_stats
            return path_stats
