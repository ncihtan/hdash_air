"""Test Meta Summary class."""
import pytest
from hdash.stats.meta_summary import MetaDataSummary
from hdash.synapse.meta_map import MetaMap


def test_meta_summary(sample_meta_map: MetaMap):
    """Test Meta Summary."""
    meta_map = sample_meta_map
    meta_list = meta_map.meta_list_sorted
    meta_summary = MetaDataSummary(meta_list)
    assert meta_list[0].meta_cache.percent_completed_fields == pytest.approx(
        0.427, 0.01
    )
    assert meta_list[2].meta_cache.percent_completed_fields == pytest.approx(0.82, 0.01)
    assert meta_summary.get_overall_percent_complete() == pytest.approx(0.76, 0.01)
