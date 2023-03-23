"""Synapse Credentials."""
from airflow.models import Variable


class DatabaseCredentials:
    """Database Credentials obtained via Airflow Environment Variables."""

    DB_USER_KEY = "HDASH_DB_USER"
    DB_PASSWORD_KEY = "HDASH_DB_PASSWORD"
    DB_HOST_KEY = "HDASH_DB_HOST"
    DB_NAME_KEY = "HDASH_DB_NAME"

    def __init__(self):
        """Construct Database Credentials."""
        self._user_name = Variable.get(self.DB_USER_KEY)
        if self._user_name is None:
            raise EnvironmentError(f"{self.DB_USER_KEY} not set.")

        self._password = Variable.get(self.DB_PASSWORD_KEY)
        if self._password is None:
            raise EnvironmentError(f"{self.DB_PASSWORD_KEY} not set.")

        self._host = Variable.get(self.DB_HOST_KEY)
        if self._host is None:
            raise EnvironmentError(f"{self.DB_HOST_KEY} not set.")

        self._db_name = Variable.get(self.DB_NAME_KEY)
        if self._db_name is None:
            raise EnvironmentError(f"{self.DB_NAME_KEY} not set.")

    @property
    def user_name(self):
        """Get Database User Name."""
        return self._user_name

    @property
    def password(self):
        """Get Database Password."""
        return self._password

    @property
    def host(self):
        """Get DB Host."""
        return self._host

    @property
    def db_name(self):
        """Get DB Name."""
        return self._db_name
