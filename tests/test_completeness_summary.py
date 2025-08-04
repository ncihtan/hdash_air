"""Test CompletenessSummary."""

from hdash.graph.graph_flattener import GraphFlattener
from hdash.stats.completeness_summary import CompletenessSummary
from hdash.graph.graph_creator import GraphCreator
from hdash.synapse.meta_map import MetaMap
from hdash.util.categories import Categories

# pyright: strict


def test_completeness_summary(sample_meta_map: MetaMap):
    """Test Completeness Summary."""
    meta_map = sample_meta_map
    graph_creator = GraphCreator("HTA1", meta_map)
    graph_flat = GraphFlattener(graph_creator.htan_graph)

    stats = CompletenessSummary("HTA1", meta_map, graph_flat)
    categories = Categories()
    assert stats.has_data("HTA3_8001", categories.DEMOGRAPHICS)
    assert stats.has_data("HTA3_8004", categories.DEMOGRAPHICS)
    assert stats.has_data("HTA3_8001_1", categories.SC_RNA_SEQ_LEVEL_1)
    assert stats.has_data("HTA3_8001_1", categories.SC_RNA_SEQ_LEVEL_2)
    assert stats.has_data("HTA3_8001_1", categories.SC_RNA_SEQ_LEVEL_3)
    assert stats.has_data("HTA3_8001_1", categories.SC_RNA_SEQ_LEVEL_4)
