"""Test HTAN Validator class."""
from io import StringIO
import pandas as pd
from hdash.graph.graph_flattener import GraphFlattener
from hdash.stats.completeness_summary import CompletenessSummary
from hdash.graph.graph_creator import GraphCreator
from hdash.util.html_matrix import HtmlMatrix
from hdash.util.matrix_util import MatrixUtil


def test_matrix_util(sample_meta_map):
    """Test Matrix Util."""
    meta_map = sample_meta_map
    graph_creator = GraphCreator("HTA1", meta_map)
    graph_flat = GraphFlattener(graph_creator.htan_graph)

    stats = CompletenessSummary("HTA1", meta_map, graph_flat)

    # Run HeatMap Util
    matrix_util = MatrixUtil("HTA1", stats)

    matrix_list = matrix_util.matrix_list
    assert len(matrix_list) == 6
    matrix0 = pd.read_csv(StringIO(matrix_list[0].content))
    matrix1 = pd.read_csv(StringIO(matrix_list[1].content))
    matrix2 = pd.read_csv(StringIO(matrix_list[2].content))

    # Validate Clinical Tiers 1,2
    assert matrix0.at[0, "ParticipantID"] == "HTA3_8001"
    assert matrix0.iat[0, 1] == 1

    # Validate Clinical Tier 3
    assert matrix1.at[0, "ParticipantID"] == "HTA3_8001"
    assert matrix1.iat[0, 1] == 0

    # Validate Single Cell Data
    assert matrix2.iat[0, 0] == "HTA3_8001_001"
    assert matrix2.iat[0, 1] == 1
    assert matrix2.iat[0, 2] == 1
    assert matrix2.iat[0, 3] == 1
    assert matrix2.iat[0, 4] == 1

    # Validate the HTML and Javascript Snippets
    html_matrix = HtmlMatrix(matrix_list[0])
    html = html_matrix.get_data_frame_html()
    assert "<th>ParticipantID</th>" in html
    counts_html = html_matrix.get_counts_html()
    assert "<td>6</td>" in counts_html

    js_data = html_matrix.get_javascript_data()
    print(js_data)
