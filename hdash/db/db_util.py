"""Database Utilities."""
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database, drop_database
from hdash.db.db_base import Base
from hdash.db.credentials import DatabaseCredentials


class DbConnection:
    """Database Connection with database engine and session objects."""

    def __init__(self):
        """Construct a new Database Connection."""
        credentials = DatabaseCredentials()
        user = credentials.user_name
        password = credentials.password
        host = credentials.host
        db_name = credentials.db_name

        # Connect Pattern:  "mysql+mysqldb://username:password@localhost/dbname"
        self.db_connect_str = f"mysql+mysqldb://{user}:{password}@{host}/{db_name}"

        self._init_db_connections()
        if not database_exists(self.db_connect_str):
            self._create_database()

    def reset_database(self):
        """Reset the database and start with a clean slate."""
        drop_database(self.db_connect_str)
        self._create_database()

    def drop_database(self):
        """Drop the database."""
        drop_database(self.db_connect_str)

    @property
    def session(self):
        """Get the Database Session."""
        return self._session

    def _create_database(self):
        print("Creating tables")
        create_database(self.db_connect_str)
        Base.metadata.create_all(self._engine)
        self._init_db_connections()

    def _init_db_connections(self):
        self._engine = create_engine(self.db_connect_str)
        self._session = Session(bind=self._engine)
