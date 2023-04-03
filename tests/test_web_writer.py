"""Test Report Writer."""
from hdash.util.web_writer import WebWriter


def test_report_writer(atlas_list):
    """Test Report Writer."""
    report_writer = WebWriter(atlas_list)
    html = report_writer.index_html
    assert html.index("Ino") > 0

    atlas_html_map = report_writer.atlas_html_map
    assert len(atlas_html_map) == 1

    with open("tests/out/index.html", "w", encoding="utf-8") as file_handler:
        file_handler.write(html)

    with open("tests/out/HTA1.html", "w", encoding="utf-8") as file_handler:
        file_handler.write(atlas_html_map["HTA1"])
