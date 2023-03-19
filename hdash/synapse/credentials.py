"""Synapse Credentials."""
from airflow.models import Variable


class SynapseCredentials:
    """Synapse Credentials obtained via Airflow Environment Variables."""

    SYNAPSE_USER_KEY = "SYNAPSE_USER"
    SYNAPSE_PASSWORD_KEY = "SYNAPSE_PASSWORD"

    def __init__(self):
        """Construct Synapse Credentials."""
        self._user_name = Variable.get(self.SYNAPSE_USER_KEY)
        if self._user_name is None:
            raise EnvironmentError(f"{self.SYNAPSE_USER_KEY} not set.")

        self._password = Variable.get(self.SYNAPSE_PASSWORD_KEY)
        if self._password is None:
            raise EnvironmentError(f"{self.SYNAPSE_PASSWORD_KEY} not set.")

    @property
    def user_name(self):
        """Get Synapse User ID."""
        return self._user_name

    @property
    def password(self):
        """Get Synapse Password."""
        return self._password
