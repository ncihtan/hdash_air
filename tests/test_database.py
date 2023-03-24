"""Smoke Tests for Database Connector."""
import pytest
from hdash.db.db_util import DbConnection
from hdash.db.atlas import Atlas
from hdash.db.atlas_stats import AtlasStats


@pytest.mark.smoke
def test_atlas():
    """Smoke Test for Atlas Table."""
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
    session.close()


@pytest.mark.smoke
def test_atlas_stats():
    """Smoke Test for Atlas Stats Table."""
    db_connection = DbConnection()
    db_connection.reset_database()
    session = db_connection.session

    # Try adding a few atlas stats
    atlas_stats1 = AtlasStats("hta1")
    atlas_stats2 = AtlasStats("hta2")
    session.add(atlas_stats1)
    session.add(atlas_stats2)
    session.commit()

    # Verify that we can get the atlas stats back
    atlas_list = session.query(AtlasStats).all()
    assert len(atlas_list) == 2
    session.close()
