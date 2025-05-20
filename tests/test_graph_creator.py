"""Test Graph Creator."""
from hdash.graph.graph_creator import GraphCreator
from hdash.graph.htan_graph import HtanGraph
from hdash.synapse.meta_map import MetaMap


def test_graph_creator(sample_meta_map: MetaMap):
    """Test Graph Creator."""
    meta_map = sample_meta_map
    graph_creator = GraphCreator("HTA1", meta_map)

    # We should have 213 nodes and 271 edges
    htan_graph = graph_creator.htan_graph
    directed_graph = htan_graph.directed_graph
    assert len(directed_graph.nodes) == 213
    assert len(directed_graph.edges) == 271

    # Verify a few nodes are in the graph
    patient_node = directed_graph.nodes["HTA3_8001"]
    assert (
        patient_node[HtanGraph.DATA_KEY].meta_file.atlas_file.synapse_id == "synapse_1"
    )
    assert (
        patient_node[HtanGraph.DATA_KEY].meta_file.atlas_file.category == "Demographics"
    )

    biospecimen_node = directed_graph.nodes["HTA3_8001_1"]
    assert (
        biospecimen_node[HtanGraph.DATA_KEY].meta_file.atlas_file.synapse_id
        == "synapse_2"
    )
    assert (
        biospecimen_node[HtanGraph.DATA_KEY].meta_file.atlas_file.category
        == "Biospecimen"
    )

    assay_node = directed_graph.nodes["HTA3_8001_4651918348"]
    assert assay_node[HtanGraph.DATA_KEY].meta_file.atlas_file.synapse_id == "synapse_3"
    assert (
        assay_node[HtanGraph.DATA_KEY].meta_file.atlas_file.category
        == "ScRNA-seqLevel1"
    )

    # Check for Specific Edges
    assert directed_graph.edges["HTA3_8001_2", "HTA3_8001_4651918348"] is not None
    assert directed_graph.edges["HTA3_8001_2", "HTA3_8001_7837535366"] is not None
    assert directed_graph.edges["HTA3_8001_1", "HTA3_8001_7837535366"] is not None

    # Verify Adjacent Edges
    adjacent_list = htan_graph.adjacent_list
    assert len(adjacent_list) == 26
