"""Test Synapse Credentials."""

from unittest import mock
from hdash.util.s3_credentials import S3Credentials


def test_s3_credentials():
    """Test S3 Credentials."""
    # Patch Airflow Variables.
    # This is a recommended practiced described at:
    # https://airflow.apache.org/docs/apache-airflow/2.0.2/best-practices.html
    airflow_vars = {
        "AIRFLOW_VAR_S3_ACCESS_KEY_ID": "key123",
        "AIRFLOW_VAR_S3_SECRET_ACCESS_KEY": "secret123",
        "AIRFLOW_VAR_S3_ENDPOINT_URL": "url123",
        "AIRFLOW_VAR_S3_BUCKET_NAME": "hdash",
        "AIRFLOW_VAR_S3_WEB_SITE_URL": "linode.com",
    }
    with mock.patch.dict("os.environ", airflow_vars):
        credentials = S3Credentials()
        assert credentials.access_key_id == "key123"
        assert credentials.secret_access_key == "secret123"
        assert credentials.endpoint_url == "url123"
        assert credentials.bucket_name == "hdash"
        assert credentials.web_site_url == "linode.com"

        s3_config = credentials.get_s3_config()
        assert "secret123" in s3_config["aws_secret_access_key"]
