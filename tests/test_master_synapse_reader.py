"""Test Master Synapse Reader."""
import pandas as pd
from hdash.reader.master_synapse_reader import MasterSynapseReader


def test_master_synapse_reader():
    """Test Master Synapse Reader."""
    synapse_df = pd.read_csv("tests/data/master_htan.csv")
    reader = MasterSynapseReader("HTA1", synapse_df)
    file_list = reader.get_file_list()

    # master_htan.csv has 11 files.
    # 2 are in archive folders
    # 1 is a legacy meta file
    # we should therefore get 8 files
    assert len(file_list) == 8
