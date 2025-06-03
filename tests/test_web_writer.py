"""Test Report Writer."""
from hdash.db.path_stats import PathStats
from hdash.util.web_writer import WebWriter
from hdash.graph.graph_flattener import GraphFlattener
from hdash.stats.completeness_summary import CompletenessSummary
from hdash.graph.graph_creator import GraphCreator
from hdash.util.matrix_util import MatrixUtil
from hdash.util.html_matrix import HtmlMatrix
from hdash.synapse.atlas_info import AtlasInfo
from hdash.synapse.meta_map import MetaMap
from hdash.db.longitudinal import Longitudinal
from hdash.util.longitudinal_util import LongitudinalUtil


def test_report_writer(atlas_list: list[AtlasInfo], sample_meta_map: MetaMap):
    """Test Report Writer."""
    graph_creator = GraphCreator("HTA1", sample_meta_map)
    graph_flat = GraphFlattener(graph_creator.htan_graph)
    stats = CompletenessSummary("HTA1", sample_meta_map, graph_flat)
    matrix_util = MatrixUtil("HTA1", stats)
    matrix_list = matrix_util.matrix_list
    html_matrix_list: list[HtmlMatrix] = []
    for matrix in matrix_list:
        html_matrix = HtmlMatrix(matrix)
        html_matrix_list.append(html_matrix)
    atlas_list[0].html_matrix_list = html_matrix_list
    path_stats_list: list[PathStats] = []
    path_stats_0 = PathStats("HTA1", "synapse123", "/")
    path_stats_0.num_annotated_files = 20
    path_stats_0.num_un_annotated_files = 40
    path_stats_list.append(path_stats_0)
    atlas_list[0].path_stats_list = path_stats_list
    atlas_list[0].longitudinal_table = _get_longitudinal_table()

    report_writer = WebWriter(atlas_list)
    html = report_writer.index_html

    atlas_html_map = report_writer.atlas_html_map
    assert len(atlas_html_map) == 1

    with open("tests/out/index.html", "w", encoding="utf-8") as file_handler:
        file_handler.write(html)

    with open("tests/out/HTA1.html", "w", encoding="utf-8") as file_handler:
        file_handler.write(atlas_html_map["HTA1"])
    assert html.index("HTAN MSKCC") > 0

def _get_longitudinal_table():
    longitudinal_util = LongitudinalUtil("HTA_1")

    therapy_data1 = _get_data("tests/data/longitudinal_therapy1.csv")
    therapy_data2 = _get_data("tests/data/longitudinal_therapy2.csv")
    biospeciman_data1 = _get_data("tests/data/longitudinal_biospecimen1.csv")
    biospeciman_data2 = _get_data("tests/data/longitudinal_biospecimen2.csv")

    longitudinal_util.build_therapy_matrix(therapy_data1)
    longitudinal_util.build_therapy_matrix(therapy_data2)
    longitudinal_util.build_biospecimen_matrix(biospeciman_data1)
    longitudinal_util.build_biospecimen_matrix(biospeciman_data2)
    longitudinal_util.create_longitudinal()

    return longitudinal_util.table_list

def _get_data(file_name: str):
    with (open(file_name, "r")) as file:
        data = file.read()
        return data