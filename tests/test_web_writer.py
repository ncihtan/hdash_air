"""Test Report Writer."""
from hdash.util.web_writer import WebWriter
from hdash.graph.graph_flattener import GraphFlattener
from hdash.stats.completeness_summary import CompletenessSummary
from hdash.graph.graph_creator import GraphCreator
from hdash.util.matrix_util import MatrixUtil
from hdash.util.html_matrix import HtmlMatrix

def test_report_writer(atlas_list, sample_meta_map):
    """Test Report Writer."""
    graph_creator = GraphCreator("HTA1", sample_meta_map)
    graph_flat = GraphFlattener(graph_creator.htan_graph)
    stats = CompletenessSummary("HTA1", sample_meta_map, graph_flat)
    matrix_util = MatrixUtil("HTA1", stats)
    matrix_list = matrix_util.matrix_list
    html_matrix_list = []
    for matrix in matrix_list:
        html_matrix = HtmlMatrix(matrix)
        html_matrix_list.append(html_matrix)
    atlas_list[0].html_matrix_list = html_matrix_list

    report_writer = WebWriter(atlas_list)
    html = report_writer.index_html

    atlas_html_map = report_writer.atlas_html_map
    assert len(atlas_html_map) == 1

    with open("tests/out/index.html", "w", encoding="utf-8") as file_handler:
        file_handler.write(html)

    with open("tests/out/HTA1.html", "w", encoding="utf-8") as file_handler:
        file_handler.write(atlas_html_map["HTA1"])
    assert html.index("Ino") > 0
