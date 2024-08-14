"""Therapy Utility."""
import pandas as pd
import numpy as np
from io import StringIO
from hdash.db.therapy import Therapy
import logging

class TherapyUtil:
    """Therapy Utility Class."""

    def __init__(self, atlas_id):
        """Create Therapy Utility."""
        self.logger = logging.getLogger("airflow.task")
        self.atlas_id = atlas_id
        self.table_list = []
        self.longitudinal = pd.DataFrame(columns=["HTAN Participant ID", "Days to Start", "Days to End", "Label"])

    def build_therapy_matrix(self, therapy_data):
        """Build Therapy Data Table."""
        # Extract therapy data into columns
        headers = ["HTAN Participant ID", "Treatment Type", "Days to Treatment End", "Days to Treatment Start"]
        try:
            data_frame = pd.read_csv(StringIO(therapy_data), usecols=headers)
        except:
            self.logger.info("Incorrectly formatted therapy file for atlas %s.", self.atlas_id)
            return
        
        data_frame = data_frame.rename(columns={"Treatment Type": "Label", "Days to Treatment End": "Days to End", "Days to Treatment Start": "Days to Start"})
        self.longitudinal = pd.concat([self.longitudinal, data_frame])

    def create_therapy(self):
        # Build string for mermaid visualization
        therapy_table = self._build_mermaid_table(self.longitudinal)
        # Create therapy object if one doesn't exist
        if len(self.table_list) == 0:
            therapy = Therapy()
            therapy.atlas_id = self.atlas_id
            therapy.label = "Longitudinal Summary"
            therapy.content = therapy_table
            self.table_list.append(therapy)
        # Append to therapy table otherwise
        else:
            self.table_list[0] += therapy_table

    def build_biospecimen_matrix(self, therapy_data):
        """Build Biospecimen Data Table."""
        # Extract biospecimen data into columns
        headers = ["HTAN Parent ID", "Collection Days from Index", "Acquisition Method Type"]
        try:
            data_frame = pd.read_csv(StringIO(therapy_data), usecols=headers)
        except:
            self.logger.info("Incorrectly formatted biospecimen file for atlas %s.", self.atlas_id)
            return

        data_frame["HTAN Parent ID"] = data_frame["HTAN Parent ID"].str.split('_').str[0:2].str.join('_')
        # Add duplicates count for each row
        data_frame["Number"] = 1
        data_frame["Number"] = data_frame.groupby(headers).transform(sum)

        # Remove duplicated rows except first one
        data_frame = data_frame.drop_duplicates(subset=headers, keep="first").reset_index(
            drop=True
        )
        self.logger.info("%s.", data_frame.head())
        for index,row in data_frame.iterrows():
            if row["Number"] > 1:
                data_frame.at[index, "Acquisition Method Type"] = f'{row["Acquisition Method Type"]} ({row["Number"]})'
        del data_frame["Number"]

        data_frame["Collection Days from Index"] = pd.to_numeric(data_frame["Collection Days from Index"], errors='coerce')

        data_frame = data_frame.rename(columns={"Acquisition Method Type": "Label", "HTAN Parent ID": "HTAN Participant ID", "Collection Days from Index": "Days to Start"})
        data_frame['Days to End'] = data_frame.loc[:, 'Days to Start']
        self.longitudinal = pd.concat([self.longitudinal, data_frame])

    def _build_mermaid_table(self, df):
        table = ""
        id = ""
        days_to_start = 0
        df.sort_values(by=["HTAN Participant ID", "Days to Start"], inplace=True)
        # Iterate through data to form rows for mermaid vizualization
        for index, row in df.iterrows():
            milestone_mark = ""
            # If we are iterating to a new participant
            if id != row["HTAN Participant ID"]:
                # Set new treatment start point
                days_to_start = row["Days to Start"]
                id = row["HTAN Participant ID"]
            # Only add if there is no data missing for the row
            if row["Label"] == row["Label"] and row["Label"] != "Not Reported" and row["Label"] != "Not Reported," and (row["Days to End"] - row["Days to Start"]) == (row["Days to End"] - row["Days to Start"]):
                treatment_length=int(row["Days to End"] - days_to_start)
                treatment_start = int(row["Days to Start"] - days_to_start)
                if treatment_length == treatment_start:
                    milestone_mark = "milestone"
                value=f'section {row["HTAN Participant ID"]}\n{row["Label"]}:{milestone_mark},{treatment_start},{treatment_length}\n'
                table += value
        return table