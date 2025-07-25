"""Synapse Connector."""


import logging
import synapseclient  # type: ignore
from hdash.reader.master_synapse_reader import MasterSynapseReader
from hdash.synapse.credentials import SynapseCredentials


class SynapseConnector:
    """Core Synapse Connector Class."""

    MASTER_HTAN_ID = "syn20446927"

    def __init__(self):
        """Construct a new Synapse Connector Class."""
        self.logger = logging.getLogger("airflow.task")
        self.syn = synapseclient.Synapse()
        self.cred = SynapseCredentials()
        self.syn.login(authToken=self.cred.password, silent=True)

    def get_atlas_files(self, atlas_id, entity_id):
        """Retrieve the Synapse Table for the Specified Atlas."""
        self.logger.info("Retrieving Synapse Table for:  %s", entity_id)
        sql = f"SELECT * FROM {self.MASTER_HTAN_ID} "
        sql += f"WHERE projectId ='{entity_id}'"
        self.logger.info("Issuing Synapse Query:  %s", sql)
        table = self.syn.tableQuery(sql)
        synapse_df = table.asDataFrame()
        self.logger.info("Got Data Frame with %d rows.", len(synapse_df.index))
        reader = MasterSynapseReader(atlas_id, entity_id, synapse_df)
        return (reader.get_file_list(), reader.root_folder_map)

    def get_cvs_table(self, synapse_id):
        """Retrieve the specified CSV table from Synapse."""
        self.logger.info("Retrieving Synapse Table:  %s", synapse_id)
        table = self.syn.get(synapse_id)
        with open(table.path, "r", encoding="utf-8") as file:
            cvs_data = file.read()
        return cvs_data
