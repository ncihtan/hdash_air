"""Therapy Utility."""
import pandas as pd
from io import StringIO
from hdash.db.therapy import Therapy
import logging

class TherapyUtil:
    """Therapy Utility Class."""

    def __init__(self, atlas_id, therapy_csv):
        """Create Therapy Utility."""
        self.logger = logging.getLogger("airflow.task")
        self.atlas_id = atlas_id
        self.therapy_csv = therapy_csv
        self.table_list = []

        # Therapy Matrix 1
        self._build_therapy_matrix(
            self.therapy_csv,
            "Therapy Summary",
        )

    def _build_therapy_matrix(self, therapy_data, label):
        """Build Therapy Data Table."""
        # Extract therapy data into columns
        headers = ["HTAN Participant ID", "Treatment Type", "Days to Treatment End", "Days to Treatment Start"]
        try:
            data_frame = pd.read_csv(StringIO(therapy_data), usecols=headers)
        except:
            self.logger.info("Incorrectly formatted therapy file for atlas %s.", self.atlas_id)
            return

        # Build string for mermaid visualization
        therapy_table = self._build_mermaid_table(data_frame)
        # Create therapy object if one doesn't exist
        if len(self.table_list) == 0:
            therapy = Therapy()
            therapy.atlas_id = self.atlas_id
            therapy.label = label
            therapy.content = therapy_table
            self.table_list.append(therapy)
        # Append to therapy table otherwise
        else:
            self.table_list[0] += therapy_table

    def _build_mermaid_table(self, df):
        table = ""
        id = ""
        days_to_start = 0
        df.sort_values(by=['HTAN Participant ID', "Days to Treatment Start"], inplace=True)
        # Iterate through data to form rows for mermaid vizualization
        for index, row in df.iterrows():
            milestone_mark = ""
            # If we are iterating to a new participant
            if id != row["HTAN Participant ID"]:
                # Set new treatment start point
                days_to_start = row["Days to Treatment Start"]
                id = row["HTAN Participant ID"]
            # Only add if there is no data missing for the row
            if row["Treatment Type"] == row["Treatment Type"] and row["Treatment Type"] != "Not Reported" and row["Treatment Type"] != "Not Reported," and (row["Days to Treatment End"] - row["Days to Treatment Start"]) == (row["Days to Treatment End"] - row["Days to Treatment Start"]):
                treatment_length=int(row["Days to Treatment End"] - days_to_start)
                treatment_start = int(row["Days to Treatment Start"] - days_to_start)
                if treatment_length == treatment_start:
                    milestone_mark = "milestone"
                value=f'section {row["HTAN Participant ID"]}\n{row["Treatment Type"]}:{milestone_mark},{treatment_start},{treatment_length}\n'
                table += value
        return table