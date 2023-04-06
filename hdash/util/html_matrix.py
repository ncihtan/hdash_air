"""HTML Matrix."""
import json
from io import StringIO
import pandas as pd
from hdash.db.matrix import Matrix


class HtmlMatrix:
    """HTML Matrix."""

    def __init__(self, matrix: Matrix):
        """Create new HTML Matrix Object."""
        self.matrix = matrix
        self.data_frame = pd.read_csv(StringIO(matrix.content))

    def get_data_frame_html(self):
        """Get Data Frame HTML."""
        return self.data_frame.to_html(
            index=False, justify="left", classes="table table-striped table-sm"
        )

    def get_counts_html(self):
        """Get Counts HTML."""
        revised_df = self._prepare_df(self.data_frame)
        counts = revised_df.sum(axis=0)
        counts_df = counts.to_frame()
        counts_df.index = list(counts.index)
        counts_df.columns = ["Counts"]
        return counts_df.to_html(
            index=True, justify="left", classes="table table-striped table-sm"
        )

    def get_javascript_data(self):
        """Get Javascript Data."""
        revised_df = self._prepare_df(self.data_frame)
        components = {
            "z": revised_df.to_numpy().tolist(),
            "x": list(revised_df.columns),
        }
        data = [components]
        return json.dumps(data)

    def _prepare_df(self, data_frame):
        """Prepare Dataframe for Heatmap Viz."""
        columns = list(data_frame.columns)
        if "BiospecimenID" in columns:
            data_frame.index = data_frame["BiospecimenID"]
            revised_df = data_frame.drop(["BiospecimenID"], axis=1)
        else:
            data_frame.index = data_frame["ParticipantID"]
            revised_df = data_frame.drop(["ParticipantID"], axis=1)
        return revised_df
