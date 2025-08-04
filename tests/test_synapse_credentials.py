"""Test Synapse Credentials."""

from unittest import mock
from hdash.synapse.credentials import SynapseCredentials


def test_synapse_credentials():
    """Test Synapse Credentials."""
    vars = {
        "SYNAPSE_USER": "user",
        "SYNAPSE_PASSWORD": "password",
    }
    with mock.patch.dict("os.environ", vars):
        credentials = SynapseCredentials()
        assert credentials.user_name == "user"
        assert credentials.password == "password"
