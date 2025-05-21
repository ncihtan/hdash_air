"""Test Longitudinal Utility."""
from hdash.util.longitudinal_util import LongitudinalUtil
from html.parser import HTMLParser

def test_longitudinal_util():
    """Test Longitudinal Util."""
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

    # Assertions
    assert not longitudinal_util.longitudinal.empty, "longitudinal DataFrame should not be empty"
    assert not longitudinal_util.longitudinal_plotly.empty, "longitudinal_plotly should not be empty"
    assert len(longitudinal_util.table_list) == 1, "Expected at least one Longitudinal object in table_list"

    # Check required columns
    required_columns = {"HTAN Participant ID", "Label", "Days to Start", "Days to End"}
    assert required_columns.issubset(longitudinal_util.longitudinal.columns), "Missing expected mermaid columns"

    plotly_columns = {"event", "id", "sample_ids", "start", "end", "location"}
    assert plotly_columns.issubset(longitudinal_util.longitudinal_plotly.columns), "Missing plotly columns"

    for longitudinal in longitudinal_util.table_list:
        # Mermaid checks
        assert isinstance(longitudinal.content, str), "Mermaid table must be string"
        assert longitudinal.content.strip().startswith("section "), "Mermaid string should start with 'section '"

        # Plotly checks
        plotly_html = longitudinal.get_html_plotly()
        _assert_valid_html(plotly_html), "Invalid Plotly figure"


def _get_data(file_name):
    with (open(file_name, "r")) as file:
        data = file.read()
        return data

class SimpleHTMLValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors = []

    def error(self, message):
        self.errors.append(message)

def _assert_valid_html(html_str):
    parser = SimpleHTMLValidator()
    parser.feed(html_str)
    assert not parser.errors, f"HTML parsing errors: {parser.errors}"