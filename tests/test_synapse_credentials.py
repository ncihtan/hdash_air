"""Test Synapse Credentials."""
import pytest
from hdash.synapse.credentials import SynapseCredentials
from unittest import mock


def test_synapse_credentials():
    """Test Synapse Credentials."""

    # Patch Airflow Variables.
    # This is a recommended practiced described at:
    # https://airflow.apache.org/docs/apache-airflow/2.0.2/best-practices.html
    airflow_vars = {
        "AIRFLOW_VAR_SYNAPSE_USER": "user",
        "AIRFLOW_VAR_SYNAPSE_PASSWORD": "password",
    }
    with mock.patch.dict("os.environ", airflow_vars):
        credentials = SynapseCredentials()
        assert "user" == credentials.user_name
        assert "password" == credentials.password
