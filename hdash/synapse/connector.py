"""Synapse Connector."""


import synapseclient  # type: ignore
from pandas import DataFrame  # type: ignore
import logging
from hdash.synapse.credentials import SynapseCredentials


class SynapseConnector:
    """Core Synapse Connector Class."""

    MASTER_HTAN_ID = "syn20446927"

    def __init__(self):
        """Construct a new Synapse Connector Class."""
        self._logger = logging.getLogger("airflow.task")
        self._syn = synapseclient.Synapse()
        self._cred = SynapseCredentials()
        self._syn.login(self._cred.user_name, self._cred.password, silent=True)

    def retrieve_atlas_table(self, entity_id):
        """Retrieve the Synapse Table for the Specified Atlas."""
        self._logger.info("Retrieving Synapse Table for:  %s." % entity_id)
        sql = f"SELECT * FROM {SynapseConnector.MASTER_HTAN_ID} WHERE projectId ='{entity_id}';"
        self._logger.info("Issuing Synapse Query:  %s" % sql)
        table = self._syn.tableQuery(sql)
        df = table.asDataFrame()
        self._logger.info("Got Data Frame with %d rows." % len(df.index))
        # df.to_csv(SynapseUtil.MASTER_HTAN_TABLE)
        return df

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
