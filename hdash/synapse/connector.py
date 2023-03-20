"""Synapse Connector."""


import logging
import synapseclient
from hdash.synapse.credentials import SynapseCredentials


class SynapseConnector:
    """Core Synapse Connector Class."""

    MASTER_HTAN_ID = "syn20446927"

    def __init__(self):
        """Construct a new Synapse Connector Class."""
        self.logger = logging.getLogger("airflow.task")
        self.syn = synapseclient.Synapse()
        self.cred = SynapseCredentials()
        self.syn.login(self.cred.user_name, self.cred.password, silent=True)

    def retrieve_atlas_table(self, entity_id):
        """Retrieve the Synapse Table for the Specified Atlas."""
        self.logger.info("Retrieving Synapse Table for:  %s", entity_id)
        sql = f"SELECT * FROM {self.MASTER_HTAN_ID} "
        sql += f"WHERE projectId ='{entity_id}';"
        self.logger.info("Issuing Synapse Query:  %s", sql)
        table = self.syn.tableQuery(sql)
        synapse_df = table.asDataFrame()
        self.logger.info("Got Data Frame with %d rows.", len(synapse_df.index))
        return synapse_df

    def retrieve_file(self, synapse_id):
        """Retrieve the specified file from Synapse."""
        print(f"To be implemented {synapse_id}.")

    # def retrieve_file(self, synapse_id):
    #     """Retrieve the specified file from Synapse."""
    #     syn_link = self.syn.get(
    #         entity=synapse_id,
    #         downloadLocation=SynapseUtil.CACHE,
    #     )
    #     new_file_path = SynapseUtil.CACHE + "/" + synapse_id + ".csv"
    #     logging.info("Renaming:  %s --> %s" % (syn_link.path, new_file_path))
    #     os.rename(syn_link.path, new_file_path)
    #     return new_file_path
