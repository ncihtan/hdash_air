"""Test Master Synapse Reader."""
import pandas as pd
from hdash.reader.master_synapse_reader import MasterSynapseReader
from hdash.synapse.file_type import FileType


def test_master_synapse_reader():
    """Test Master Synapse Reader."""
    synapse_df = pd.read_csv("tests/data/master_htan.csv")
    reader = MasterSynapseReader("HTA1", synapse_df)
    file_list = reader.get_file_list()

    # master_htan.csv has 11 files.
    # 3 are in archive folders
    # 1 is a legacy meta file
    # 1 is a .DS_Store file
    # we also have two meta files in the same directory
    # only one of this should be chosen.
    # we therefore end up with 5 files
    assert len(file_list) == 5

    # Verify that we get the correct, most recent meta file
    file0 = file_list[0]
    assert file0.data_type == FileType.METADATA.value
