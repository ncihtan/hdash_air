"""Smoke Tests for Synapse Connector."""
import pytest
from hdash.synapse.connector import SynapseConnector


@pytest.mark.smoke
def test_synapse_connector():
    """Smoke Test for Synapse Connector."""
    connector = SynapseConnector()
    (file_list, root_folder_map) = connector.get_atlas_files("HTA1", "syn23511954")
    assert len(file_list) > 0

    csv_data = connector.get_cvs_table("syn51185203")
    assert "Fixative Type" in csv_data
