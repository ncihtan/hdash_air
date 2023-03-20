import pytest
from hdash.synapse.connector import  SynapseConnector

@pytest.mark.smoke
def test_synapse_connector():
    """Test Synapse Connector."""
    connector = SynapseConnector()
    dfci_df = connector.retrieve_atlas_table("syn23511954")
    assert len(dfci_df.index) > 0
