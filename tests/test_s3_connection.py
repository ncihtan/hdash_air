"""Smoke Tests for S3 Connection"""
import pytest
import boto3
from hdash.util.s3_credentials import S3Credentials


@pytest.mark.smoke
def test_s3_connection():
    """Smoke Test for S3 Connection."""
    s3_credentials = S3Credentials()
    s3_config = s3_credentials.get_s3_config()
    client = boto3.client("s3", **s3_config)
    response = client.list_buckets()

    hdash_bucket_exists = False
    for bucket in response["Buckets"]:
        if bucket["Name"] == "hdash":
            hdash_bucket_exists = True
    assert hdash_bucket_exists
