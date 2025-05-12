"""Smoke Tests for Database Connector."""

import pytest
from hdash.db.db_util import DbConnection
from hdash.db.atlas import Atlas
from hdash.db.atlas_file import AtlasFile
from hdash.db.atlas_stats import AtlasStats
from hdash.db.meta_cache import MetaCache
from hdash.db.matrix import Matrix
from hdash.db.web_cache import WebCache
from hdash.db.validation import Validation, ValidationError


@pytest.fixture(scope="module", autouse=True)
def reset_database():
    """Start with clean slate database."""
    db_connection = DbConnection()
    db_connection.reset_database()


@pytest.mark.smoke
def test_atlas():
    """Smoke Test for Atlas Table."""
    db_connection = DbConnection()
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


@pytest.mark.smoke
def test_validation():
    """Smoke Test for Validation Checks."""
    db_connection = DbConnection()
    session = db_connection.session

    # Add a validation with multiple error messages
    validation = Validation("HTA1", "H_LINKS", "Check Links")

    error1 = ValidationError()
    error1.error_msg = "Link1 failed"
    validation.error_list.append(error1)

    error2 = ValidationError()
    error2.error_msg = "Link2 failed"
    validation.error_list.append(error2)

    session.add(validation)
    session.commit()

    # Verify that we can get the objects back
    validation_list = session.query(Validation).all()
    assert len(validation_list) == 1
    record0 = validation_list[0]
    assert len(record0.error_list) == 2
    session.close()


@pytest.mark.smoke
def test_matrix():
    """Smoke Test for Matrix."""
    db_connection = DbConnection()
    session = db_connection.session

    matrix = Matrix()
    matrix.matrix_id = "hta1_clinical"
    matrix.atlas_id = "HTA1"
    matrix.order = 0
    matrix.label = "Clinical Demographics"
    session.add(matrix)

    # Verify that we can get the objects back
    matrix_list = session.query(Matrix).all()
    assert len(matrix_list) == 1


@pytest.mark.smoke
def test_web_cache():
    """Smoke Test for Web Cache."""
    db_connection = DbConnection()
    session = db_connection.session

    web_cache = WebCache()
    web_cache.file_name = "index.html"
    web_cache.content = "<html>Page</html>"
    session.add(web_cache)

    # Verify that we can get the objects back
    web_cache_list = session.query(WebCache).all()
    assert len(web_cache_list) == 1
