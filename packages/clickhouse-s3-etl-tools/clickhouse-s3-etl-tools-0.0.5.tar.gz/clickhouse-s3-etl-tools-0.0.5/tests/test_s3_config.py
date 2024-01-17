import unittest
from unittest.mock import MagicMock

from clickhouse_s3_etl_tools.exceptions.exception import S3Error
from clickhouse_s3_etl_tools.schema.schema_configs import S3Config, TableConfiguration
from clickhouse_s3_etl_tools.connectors.s3_connector import S3Connector

bucket = "testnew2/test2s"
endpoint = "http://localhost:9002"
aws_access_key_id = "minio_access_key"
aws_secret_access_key = "minio_secret_key"


class TestS3Connector(unittest.TestCase):
    def setUp(self):
        self.s3_config = S3Config(
            PATH_S3=f"{endpoint}/{bucket}",
            S3_ACCESS_KEY=aws_access_key_id,
            S3_SECRET_KEY=aws_secret_access_key
        )
        self.s3_connector = S3Connector(self.s3_config)

    def test_init(self):
        self.assertEqual(self.s3_connector.bucket_name, bucket.split('/')[0])
        self.assertEqual(self.s3_connector.config["aws_access_key_id"], aws_access_key_id)
        self.assertEqual(self.s3_connector.config["aws_secret_access_key"], aws_secret_access_key)
        self.assertEqual(self.s3_connector.config["endpoint_url"], endpoint)
        self.assertEqual(self.s3_connector.config["service_name"], "s3")

    def test_enter(self):
        self.s3_connector.session = MagicMock()
        self.s3_connector.session.client.return_value = MagicMock()
        self.s3_connector.session.resource.return_value = MagicMock()

        # self.s3_connector.s3_client.head_bucket.side_effect = None
        # self.s3_connector.s3_client.list_buckets.side_effect = None

        with self.s3_connector as connector:
            self.assertEqual(connector, self.s3_connector)
            self.s3_connector.session.client.assert_called_with(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                endpoint_url=endpoint,
                service_name="s3"
            )
            self.s3_connector.session.resource.assert_called_with(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                endpoint_url=endpoint,
                service_name="s3"
            )
            self.s3_connector.s3_client.head_bucket.assert_called_with(Bucket="my-bucket")

    def test_enter_s3_error(self):
        self.s3_connector.session = MagicMock()
        self.s3_connector.session.client.return_value = MagicMock()
        self.s3_connector.session.resource.return_value = MagicMock()

        self.s3_connector.s3_client.head_bucket.side_effect = S3Error(url=self.s3_connector.config["endpoint_url"], message="Can't connect to S3")

        with self.assertRaises(S3Error):
            with self.s3_connector:
                pass

    # Add more test cases for the other methods in the S3Connector class


if __name__ == "__main__":
    unittest.main()
