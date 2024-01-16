import logging
import unittest

from clickhouse_s3_etl_tools.connectors import clickhouse_connector, s3_connector
from clickhouse_s3_etl_tools.schema.schema_configs import Configuration, S3Config, TableConfiguration
from clickhouse_s3_etl_tools.exceptions.exception import S3Error
from helper_for_tests import create_database, create_and_fill_table
from clickhouse_s3_etl_tools.schema.schema_table_metadata import MetadataConfig
from clickhouse_s3_etl_tools.s3_exporter.s3_exporter import export_to_s3, GROUP_BY_PARTS_SQL, fetch_number_rows_from_s3
from clickhouse_s3_etl_tools.s3_to_clickhouse_transfer.s3_to_clickhouse_transfer import transfer_s3_to_clickhouse, \
    fetch_metadata_from_s3


class BaseIntegrationTest(unittest.TestCase):
    config_table_metadata = None
    mock_config_table_metadata = None
    mock_config = None

    @classmethod
    def setUpClass(cls):
        """Initialize mock objects and set up configuration for table creation."""
        cls.mock_config = Configuration(
            clickhouse={
                "CH_URL_SOURCE": "clickhouse+native://default:default@localhost:9000/default",
                "CH_URL_DESTINATION": "clickhouse+native://default2:default2@localhost:9003/default",
            },
            s3={
                "PATH_S3": "http://localhost:9002/testnew2",
                "S3_ACCESS_KEY": "minio_access_key",
                "S3_SECRET_KEY": "minio_secret_key",
            },
            table={
                "DATABASE": "test",
                "DATABASE_DESTINATION": "test2",
                "TABLE_NAME": "test_table"
            },
            BATCH_SIZE=10,
            DROP_DESTINATION_TABLE_IF_EXISTS=True,
        )

        cls.config_table_metadata = {
            "create_table_query": "",
            "engine": "MergeTree",
            "partition_key": "dt",
            "total_rows": 100,
            "check_sum_column_name": "column2"
        }

        create_and_fill_table(
            cls.mock_config.clickhouse.CH_URL_SOURCE,
            cls.mock_config.table,
            cls.config_table_metadata,
            count_parts=cls.config_table_metadata["total_rows"] / cls.mock_config.BATCH_SIZE,
        )

        cls.create_bucket_clear_directory(cls.mock_config.s3, cls.mock_config.table)
        create_database(cls.mock_config.clickhouse.CH_URL_SOURCE,
                        cls.mock_config.table)
        export_to_s3(cls.mock_config)
        transfer_s3_to_clickhouse(cls.mock_config)


    @staticmethod
    def create_bucket_clear_directory(s3_config: S3Config, table_config: TableConfiguration):
        """Create bucket if not exists and clear directory."""
        with s3_connector.S3Connector(s3_config) as s3_conn:
            s3_conn.create_bucket_if_not_exists()
            s3_conn.drop_table_directory_if_exists(table_config)

    def test_fake_s3(self):
        """Test fake S3 connections."""
        s3_config = S3Config(
            PATH_S3="http://localhost:9002/testnewtest",
            S3_ACCESS_KEY="minio_access_key",
            S3_SECRET_KEY="minio_secret_key",
        )
        with s3_connector.S3Connector(s3_config):
            pass

        s3_config = S3Config(
            PATH_S3="http://localhost:9002/testnewtest",
            S3_ACCESS_KEY="fakeaccess_key",
            S3_SECRET_KEY="minio_secret_key",
        )
        with self.assertRaises(S3Error) as context:
            with s3_connector.S3Connector(s3_config):
                print(context)

        s3_config = S3Config(
            PATH_S3="http://fakeurl:9000/testnewtest",
            S3_ACCESS_KEY="fakeaccess_key",
            S3_SECRET_KEY="minio_secret_key",
        )
        with self.assertRaises(S3Error) as context:
            with s3_connector.S3Connector(s3_config):
                print(context)

    def test_filling_table(self):
        """Check that the table contains the required number of rows."""
        with clickhouse_connector.ClickHouseConnector(
                self.mock_config.clickhouse.CH_URL_SOURCE
        ) as conn:
            res = conn.client.execute(
                f"select count(*) from {self.mock_config.table.DATABASE}.{self.mock_config.table.TABLE_NAME}"
            )
            number_rows = next((column[0] for column in res if res), None)

        self.assertEqual(self.config_table_metadata["total_rows"], number_rows)

    def test_split_by_parts(self):
        """Check splitting table by parts."""
        with clickhouse_connector.ClickHouseConnector(
                self.mock_config.clickhouse.CH_URL_SOURCE
        ) as conn:
            metadata: MetadataConfig = conn.get_table_metadata(self.mock_config.table.DATABASE,
                                                               self.mock_config.table.TABLE_NAME)

            if metadata.partition_key == "" or metadata.partition_key == "tuple()":
                return

            res = conn.fetch_rows_by_cumulative_sum(
                GROUP_BY_PARTS_SQL.format(
                    partition_key=metadata.partition_key,
                    table_name=self.mock_config.table.TABLE_NAME,
                    database=self.mock_config.table.DATABASE,
                ),
                self.mock_config.BATCH_SIZE,
            )

            self.assertEqual(
                metadata.total_rows, sum([r[2] for r in res])
            )
            self.assertEqual(self.mock_config.BATCH_SIZE, max([r[2] for r in res]))

    def test_export_to_s3(self):
        """Check exporting to S3."""
        with clickhouse_connector.ClickHouseConnector(
                self.mock_config.clickhouse.CH_URL_SOURCE
        ) as conn:
            self.assertEqual(
                self.config_table_metadata["total_rows"],
                fetch_number_rows_from_s3(
                    self.mock_config, conn
                ),
            )

    def test_transfer_to_clickhouse_metadata(self):
        """Check transferring metadata to ClickHouse."""
        with clickhouse_connector.ClickHouseConnector(
                self.mock_config.clickhouse.CH_URL_DESTINATION
        ) as conn_dest, clickhouse_connector.ClickHouseConnector(
            self.mock_config.clickhouse.CH_URL_SOURCE
        ) as conn_source:
            metadata_s3: MetadataConfig = fetch_metadata_from_s3(
                self.mock_config, conn_dest
            )
            metadata_ch_source: MetadataConfig = conn_source.get_table_metadata(self.mock_config.table.DATABASE,
                                                                                self.mock_config.table.TABLE_NAME)

            self.assertEqual(metadata_s3, metadata_ch_source)

    def assert_table_row_count_equal(
            self, conn1, conn2, database_dest, database_source, table
    ):
        """Assert that row counts for two tables are equal."""
        query1 = f"SELECT count(*) FROM {database_dest}.{table}"
        query2 = f"SELECT count(*) FROM {database_source}.{table}"
        rows1 = conn1.client.execute(query1)
        rows2 = conn2.client.execute(query2)

        count1 = next((column[0] for column in rows1 if rows1), None)
        count2 = next((column[0] for column in rows2 if rows2), None)

        self.assertEqual(
            count1,
            count2,
            f"Row counts for {database_dest}.{table} and  {database_source}.{table}  do not match.",
        )

    def assert_table_sum_equal(
            self, conn1, conn2, database_dest, database_source, table, column_sum
    ):
        """Assert that sums for two tables are equal."""
        query1 = f"SELECT sum({column_sum}) FROM {database_dest}.{table}"
        query2 = f"SELECT sum({column_sum}) FROM {database_source}.{table}"
        logging.info(query1)
        logging.info(query2)
        rows1 = conn1.client.execute(query1)
        rows2 = conn2.client.execute(query2)

        sum1 = next((column[0] for column in rows1 if rows1), None)
        sum2 = next((column[0] for column in rows2 if rows2), None)

        self.assertEqual(
            sum1,
            sum2,
            f"Sum for {database_dest}.{table} and  {database_source}.{table}  do not match.",
        )

    def test_transfer_to_clickhouse(self):
        """Check transferring data to ClickHouse."""
        with clickhouse_connector.ClickHouseConnector(
                self.mock_config.clickhouse.CH_URL_DESTINATION
        ) as conn_dest, clickhouse_connector.ClickHouseConnector(
            self.mock_config.clickhouse.CH_URL_SOURCE
        ) as conn_source:
            self.assert_table_row_count_equal(
                conn_dest,
                conn_source,
                self.mock_config.table.DATABASE_DESTINATION,
                self.mock_config.table.DATABASE,
                self.mock_config.table.TABLE_NAME,
            )

            self.assert_table_sum_equal(
                conn_dest,
                conn_source,
                self.mock_config.table.DATABASE_DESTINATION,
                self.mock_config.table.DATABASE,
                self.mock_config.table.TABLE_NAME,
                column_sum=self.config_table_metadata["check_sum_column_name"],
            )
