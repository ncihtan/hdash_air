"""Smoke Tests for Database Connector."""
import pytest
from hdash.db.db_util import DbConnection
from hdash.db.atlas import Atlas


@pytest.mark.smoke
def test_database():
    """Smoke Test for Database."""
    db_connection = DbConnection()
    db_connection.reset_database()
    session = db_connection.session

    # Try adding a few atlases
    atlas1 = Atlas("hta1", "dfci", "s1", "Ethan Cerami")
    atlas2 = Atlas("hta2", "bu", "s2", "Ethan Cerami")
    session.add(atlas1)
    session.add(atlas2)
    session.commit()

    # Verify that we can get the atlases back
    atlas_list = session.query(Atlas).all()
    assert len(atlas_list) == 2
