"""Test Longitudinal Utility."""
from hdash.util.longitudinal_util import LongitudinalUtil


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


def _get_data(file_name):
    with (open(file_name, "r")) as file:
        data = file.read()
        return data
