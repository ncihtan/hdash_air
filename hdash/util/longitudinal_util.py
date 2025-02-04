"""Longitudinal Utility."""
import json
import logging
import pandas as pd
from io import StringIO
from hdash.db.longitudinal import Longitudinal


class LongitudinalUtil:
    """Therapy Utility Class."""

    def __init__(self, atlas_id):
        """Create Longitudinal Utility."""
        self.logger = logging.getLogger("airflow.task")
        self.atlas_id = atlas_id
        self.table_list = []
        self.plotly_list = []
        self.longitudinal = pd.DataFrame(
            columns=["HTAN Participant ID", "Days to Start", "Days to End", "Label"]
        )
        self.longitudinal_plotly = pd.DataFrame(
            columns=["event", "id", "sample_ids", "start", "end", "location"]
        )

    def build_therapy_matrix(self, therapy_data):
        """Build Therapy Data Table."""
        # Extract therapy data into columns
        headers = [
            "HTAN Participant ID",
            "Treatment Type",
            "Days to Treatment End",
            "Days to Treatment Start",
            "Treatment Anatomic Site",
        ]
        data_frame = pd.read_csv(StringIO(therapy_data), usecols=headers)

        data_frame = data_frame.rename(
            columns={
                "Treatment Type": "Label",
                "Days to Treatment End": "Days to End",
                "Days to Treatment Start": "Days to Start",
            }
        )
        self.longitudinal = pd.concat([self.longitudinal, data_frame])

        # Pull out the therapy data into the plotly dataframe
        plotly_data = dict(
            event=[], id=[], sample_ids=[], start=[], end=[], location=[]
        )
        for index, row in data_frame.iterrows():
            plotly_data["event"].append(row["Label"])
            plotly_data["id"].append(f'{row["HTAN Participant ID"]} Therapy')
            plotly_data["sample_ids"].append("NA")
            plotly_data["start"].append(row["Days to Start"])
            plotly_data["end"].append(row["Days to End"])
            plotly_data["location"].append("NA")
        plotly_df = pd.DataFrame.from_dict(plotly_data, orient="index").transpose()
        self.longitudinal_plotly = pd.concat([self.longitudinal_plotly, plotly_df])

    def create_longitudinal(self):
        """Build string for mermaid visualization."""
        longitudinal_table = self._build_mermaid_table(self.longitudinal)
        # Build json for plotly visualization
        plotly_json = self._build_plotly_json(self.longitudinal_plotly)
        # Create therapy object
        longitudinal = Longitudinal()
        longitudinal.atlas_id = self.atlas_id
        longitudinal.label = "Longitudinal Summary"
        longitudinal.content = longitudinal_table
        longitudinal.content_plotly = plotly_json
        self.table_list.append(longitudinal)

    def build_biospecimen_matrix(self, biospecimen_data):
        """Build Biospecimen Data Table."""
        # Extract biospecimen data into columns
        headers = [
            "HTAN Biospecimen ID",
            "HTAN Parent ID",
            "Collection Days from Index",
            "Acquisition Method Type",
            "Site of Resection or Biopsy",
            "Site Data Source",
            "Specimen Laterality",
        ]
        data_frame = pd.read_csv(StringIO(biospecimen_data), usecols=headers)
        headers.remove("HTAN Biospecimen ID")

        # Remove the derived sample rows
        pattern_derived = "^.*_.*_.*$"
        derived = data_frame["HTAN Parent ID"].str.contains(pattern_derived)
        data_frame = data_frame[~derived]

        # Separate out the sample number part of the ID
        data_frame["HTAN Biospecimen ID"] = (
            data_frame["HTAN Biospecimen ID"].str.split("_").str[2]
        )

        # Blank out malformed/missing data
        data_frame[
            ["Site of Resection or Biopsy", "Site Data Source", "Specimen Laterality"]
        ] = data_frame[
            ["Site of Resection or Biopsy", "Site Data Source", "Specimen Laterality"]
        ].fillna(
            ""
        )
        data_frame.loc[
            (data_frame["Specimen Laterality"] == "Not Applicable")
            | (data_frame["Specimen Laterality"] == "unknown")
            | (data_frame["Specimen Laterality"] == "Not Reported"),
            "Specimen Laterality",
        ] = ""
        data_frame.loc[
            (data_frame["Site of Resection or Biopsy"] == "Not Reported"),
            "Site of Resection or Biopsy",
        ] = ""

        # Add duplicates count for each row
        data_frame["Number"] = 1
        data_frame["Number"] = data_frame.groupby(headers).transform(sum)

        # Force collection days to numeric value
        data_frame["Collection Days from Index"] = pd.to_numeric(
            data_frame["Collection Days from Index"], errors="coerce"
        )

        # Make copy of data to form into plotly df
        data_frame_plotly = data_frame.copy()

        # Remove duplicated rows except first one
        data_frame = data_frame.drop_duplicates(
            subset=headers, keep="first"
        ).reset_index(drop=True)

        # Add sample list for timepoint
        plotly_headers = [
            "HTAN Parent ID",
            "Collection Days from Index",
            "Acquisition Method Type",
            "Site Data Source",
            "Site of Resection or Biopsy",
        ]

        data_frame_plotly["HTAN Biospecimen ID"] = data_frame_plotly.groupby(
            plotly_headers
        )["HTAN Biospecimen ID"].transform(lambda x: [x.tolist()] * len(x))

        # Remove duplicated rows except first one
        data_frame_plotly = data_frame_plotly.drop_duplicates(
            subset=plotly_headers, keep="first"
        ).reset_index(drop=True)

        # Build plotly data
        plotly_data = dict(
            event=[], id=[], sample_ids=[], start=[], end=[], location=[]
        )
        for index, row in data_frame_plotly.iterrows():
            plotly_data["event"].append(row["Acquisition Method Type"])
            plotly_data["id"].append(
                row["HTAN Parent ID"] + " " + row["Site of Resection or Biopsy"]
            )
            plotly_data["sample_ids"].append(row["HTAN Biospecimen ID"])
            plotly_data["start"].append(row["Collection Days from Index"])
            plotly_data["end"].append(row["Collection Days from Index"])
            plotly_data["location"].append(row["Site Data Source"])
        plotly_df = pd.DataFrame.from_dict(plotly_data, orient="index").transpose()
        self.longitudinal_plotly = pd.concat([self.longitudinal_plotly, plotly_df])

        # Build label for mermaid biospecimen
        for index, row in data_frame.iterrows():
            if row["Number"] > 1:
                data_frame.at[index, "Acquisition Method Type"] = (
                    f'{(row["Specimen Laterality"])}'
                    f' {row["Acquisition Method Type"]}'
                    f' ({row["Number"]})'
                )
            else:
                data_frame.at[
                    index, "Acquisition Method Type"
                ] = f'{(row["Specimen Laterality"])} {row["Acquisition Method Type"]}'
        del data_frame["Number"]

        data_frame["HTAN Parent ID"] = (
            data_frame["HTAN Parent ID"]
            + " "
            + data_frame["Site of Resection or Biopsy"]
        )
        data_frame = data_frame.rename(
            columns={
                "HTAN Parent ID": "HTAN Participant ID",
                "Acquisition Method Type": "Label",
                "Collection Days from Index": "Days to Start",
            }
        )
        data_frame["Days to End"] = data_frame.loc[:, "Days to Start"]
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
            if (
                row["Label"] == row["Label"]
                and row["Label"] != "Not Reported"
                and row["Label"] != "Not Reported,"
                and (row["Days to End"] - row["Days to Start"])
                == (row["Days to End"] - row["Days to Start"])
            ):
                treatment_length = int(row["Days to End"] - days_to_start)
                treatment_start = int(row["Days to Start"] - days_to_start)
                if treatment_length == treatment_start:
                    milestone_mark = "milestone"
                value = (
                    f'section {row["HTAN Participant ID"]}\n{row["Label"]}:'
                    f"{milestone_mark},{treatment_start},{treatment_length}\n"
                )
                table += value
        return table

    def _build_plotly_json(self, df):
        days_to_start = 0
        df.sort_values(by=["id", "start"], inplace=True)
        data = []
        id = ""
        for index, row in df.iterrows():
            # If we are iterating to a new participant
            if id != row["id"]:
                # Set new treatment start point
                days_to_start = row["start"]
                id = row["id"]
            # Only add if there is no data missing for the row
            if (
                row["event"] == row["event"]
                and row["event"] != "Not Reported"
                and row["event"] != "Not Reported,"
                and (row["end"] - row["start"]) == (row["end"] - row["start"])
            ):
                treatment_end = int(row["end"] - days_to_start)
                treatment_start = int(row["start"] - days_to_start)
                if treatment_end == treatment_start:
                    treatment_end += 1
                data.append(
                    dict(
                        Event=row["event"],
                        Start=treatment_start,
                        Finish=treatment_end,
                        Grouping=row["id"],
                        Samples=row["sample_ids"],
                        Location=row["location"],
                    )
                )
        return json.dumps(data)
