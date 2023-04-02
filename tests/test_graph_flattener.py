"""Test Graph Util class."""
from hdash.graph.htan_graph import HtanGraph
from hdash.graph.node_data import NodeData
from hdash.db.atlas_file import AtlasFile
from hdash.db.meta_cache import MetaCache
from hdash.graph.graph_flattener import GraphFlattener
from hdash.util.categories import Categories
from hdash.synapse.meta_file import MetaFile


def test_graph_flattener():
    """Test Graph Flattener."""
    # Create Mock Graph
    htan_graph = HtanGraph()

    p1_meta_file = _create_mock_meta_file("synapse1", Categories.DEMOGRAPHICS)
    htan_graph.add_node(NodeData("p1", p1_meta_file))

    b1_meta_file = _create_mock_meta_file("synapse2", Categories.BIOSPECIMEN)
    htan_graph.add_node(NodeData("b1", b1_meta_file))

    b2_meta_file = _create_mock_meta_file("synapse3", Categories.BIOSPECIMEN)
    htan_graph.add_node(NodeData("b2", b2_meta_file))

    b3_meta_file = _create_mock_meta_file("synapse4", Categories.BIOSPECIMEN)
    htan_graph.add_node(NodeData("b3", b3_meta_file))

    s1_meta = _create_mock_meta_file("synapse5", Categories.SC_RNA_SEQ_LEVEL_1)
    htan_graph.add_node(NodeData("s1", s1_meta))

    s2_meta = _create_mock_meta_file("synapse6", Categories.SC_RNA_SEQ_LEVEL_2)
    htan_graph.add_node(NodeData("s2", s2_meta))

    s3_meta = _create_mock_meta_file("synapse7", Categories.SC_RNA_SEQ_LEVEL_3)
    htan_graph.add_node(NodeData("s3", s3_meta))

    htan_graph.add_edge("p1", "b1")
    htan_graph.add_edge("p1", "b3")
    htan_graph.add_edge("b1", "b2")
    htan_graph.add_edge("b2", "s1")
    htan_graph.add_edge("s1", "s2")
    htan_graph.add_edge("s2", "s3")
    htan_graph.add_edge("b3", "s3")

    # Now Flatten
    graph_flat = GraphFlattener(htan_graph)

    # We should have 1 patient and 3 biospecimens
    assert len(graph_flat.participant_id_set) == 1
    assert len(graph_flat.biospecimen_id_set) == 3

    # p1 should point to b1, b2, b3
    biospecimen_list = graph_flat.participant_2_biopsecimens["p1"]
    assert len(biospecimen_list) == 3
    assert "b1" in biospecimen_list
    assert "b2" in biospecimen_list
    assert "b3" in biospecimen_list

    # b1 should not have any assays
    categories = Categories()
    assert not graph_flat.biospecimen_has_assay("b1", categories.SC_RNA_SEQ_LEVEL_1)
    assert not graph_flat.biospecimen_has_assay("b1", categories.SC_RNA_SEQ_LEVEL_2)
    assert not graph_flat.biospecimen_has_assay("b1", categories.SC_RNA_SEQ_LEVEL_3)

    # b2 should have SCRNA-Seq Levels 1-3
    assert graph_flat.biospecimen_has_assay("b2", categories.SC_RNA_SEQ_LEVEL_1)
    assert graph_flat.biospecimen_has_assay("b2", categories.SC_RNA_SEQ_LEVEL_2)
    assert graph_flat.biospecimen_has_assay("b2", categories.SC_RNA_SEQ_LEVEL_3)


def _create_mock_meta_file(synapse_id, category):
    atlas_file = AtlasFile()
    atlas_file.synapse_id = synapse_id
    atlas_file.category = category
    meta_cache = MetaCache()
    meta_file = MetaFile(atlas_file, meta_cache)
    return meta_file
