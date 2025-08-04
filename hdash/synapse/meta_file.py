"""Metadata File."""

from io import StringIO
import pandas as pd
from hdash.db.atlas_file import AtlasFile
from hdash.db.meta_cache import MetaCache


class MetaFile:
    """Encapsulates an HTAN Metadata File."""

    def __init__(self, atlas_file: AtlasFile, meta_cache: MetaCache):
        """Construct new Metadata File."""
        self.atlas_file = atlas_file
        self.meta_cache = meta_cache
        self.data_frame = None

        if meta_cache.content is not None:
            cvs_string_io = StringIO(meta_cache.content)  # type: ignore
            self.data_frame = pd.read_csv(cvs_string_io)
            self.meta_cache.num_records = len(self.data_frame.index)

    def __repr__(self):
        """Return summary of object."""
        return f"{self.atlas_file.synapse_id}: {self.atlas_file.category}"
