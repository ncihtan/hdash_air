"""S3 Credentials."""
import boto3
from airflow.models import Variable


class S3Credentials:
    """S3 Credentials obtained via Airflow Environment Variables."""

    ACCESS_KEY_ID = "S3_ACCESS_KEY_ID"
    SECRET_ACCESS_KEY = "S3_SECRET_ACCESS_KEY"
    ENDPOINT_URL = "S3_ENDPOINT_URL"
    BUCKET_NAME = "S3_BUCKET_NAME"

    def __init__(self):
        """Construct S3 Credentials."""
        self._access_key_id = Variable.get(self.ACCESS_KEY_ID)
        if self._access_key_id is None:
            raise EnvironmentError(f"{self.ACCESS_KEY_ID} not set.")

        self._secret_access_key = Variable.get(self.SECRET_ACCESS_KEY)
        if self._secret_access_key is None:
            raise EnvironmentError(f"{self.SECRET_ACCESS_KEY} not set.")

        self._endpoint_url = Variable.get(self.ENDPOINT_URL)
        if self._endpoint_url is None:
            raise EnvironmentError(f"{self.ENDPOINT_URL} not set.")

        self._bucket_name = Variable.get(self.BUCKET_NAME)
        if self._bucket_name is None:
            raise EnvironmentError(f"{self.BUCKET_NAME} not set.")

    @property
    def access_key_id(self):
        """Get Access Key ID."""
        return self._access_key_id

    @property
    def secret_access_key(self):
        """Get Secret Access Key."""
        return self._secret_access_key

    @property
    def endpoint_url(self):
        """Get Endpoint URL."""
        return self._endpoint_url

    @property
    def bucket_name(self):
        """Get Bucket Name."""
        return self._bucket_name

    def get_s3_config(self):
        """Get S3 Configuration Map."""
        s3_config = {
            "aws_access_key_id": self.access_key_id,
            "aws_secret_access_key": self.secret_access_key,
            "endpoint_url": self.endpoint_url,
        }
        return s3_config
