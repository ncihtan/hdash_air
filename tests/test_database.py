"""Smoke Tests for Database Connector."""
import pytest
from hdash.db.db_util import DbConnection
from hdash.db.atlas import Atlas
from hdash.db.atlas_file import AtlasFile
from hdash.db.atlas_stats import AtlasStats
from hdash.db.meta_cache import MetaCache


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


@pytest.mark.smoke
def test_atlas_files():
    """Smoke Test for AtlasFile Table."""
    db_connection = DbConnection()
    db_connection.reset_database()
    session = db_connection.session

    # Try adding a few atlas files
    atlas_file1 = AtlasFile()
    atlas_file1.atlas_id = "HTA1"
    atlas_file1.synapse_id = "synapse1"
    atlas_file2 = AtlasFile()
    atlas_file2.atlas_id = "HTA1"
    atlas_file2.synapse_id = "synapse2"

    session.add(atlas_file1)
    session.add(atlas_file2)
    session.commit()

    # Verify that we can get the objects
    file_list = session.query(AtlasFile).all()
    assert len(file_list) == 2
    session.close()


@pytest.mark.smoke
def test_meta_cache():
    """Smoke Test for MetaCache Table."""
    db_connection = DbConnection()
    db_connection.reset_database()
    session = db_connection.session

    # Try adding a few meta-caches
    cache1 = MetaCache()
    cache1.synapse_id = "syn1"
    cache1.md5 = "md1"

    cache2 = MetaCache()
    cache2.synapse_id = "syn2"
    cache2.md5 = "md2"

    session.add(cache1)
    session.add(cache2)
    session.commit()

    # Verify that we can get the caches back
    cache_list = session.query(MetaCache).all()
    assert len(cache_list) == 2
    session.close()
