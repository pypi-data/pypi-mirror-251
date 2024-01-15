from typing import Optional

from pydantic import BaseModel, PositiveInt


class ClickHouseConfig(BaseModel):
    """
    Pydantic model for ClickHouse configuration.

    Attributes:
        CH_URL_SOURCE (Optional[str]): ClickHouse source URL.
        CH_URL_DESTINATION (Optional[str]): ClickHouse destination URL.
    """

    CH_URL_SOURCE: str
    CH_URL_DESTINATION: str


class S3Config(BaseModel):
    """
    Pydantic model for S3 configuration.

    Attributes:
        S3_ACCESS_KEY (str): S3 access key.
        S3_SECRET_KEY (str): S3 secret key.
        PATH_S3 (str): S3 path.
    """

    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    PATH_S3: str


class TableConfiguration(BaseModel):
    """
    Pydantic model for table configuration.

    Attributes:
        TABLE_NAME (str): Table name.
        DATABASE (str): Database name.
        DATABASE_DESTINATION (str): Destination database name.
    """

    TABLE_NAME: str
    DATABASE: str
    DATABASE_DESTINATION: str


class Configuration(BaseModel):
    """
    Pydantic model for the overall configuration.

    Attributes:
        s3 (S3Config): S3 configuration.
        clickhouse (ClickHouseConfig): ClickHouse configuration.
        table (TableConfiguration): Table configuration.
        LOG_LEVEL (str): Logging level (default: INFO).
        BATCH_SIZE (PositiveInt): Batch size for processing (default: 100000000).
        DROP_DESTINATION_TABLE_IF_EXISTS (bool): Whether to drop the destination table if it exists (default: False).
        ON_CLUSTER_DIRECTIVE (str): Directive for cluster configuration (default: "").
    """

    s3: S3Config
    clickhouse: ClickHouseConfig
    table: TableConfiguration
    LOG_LEVEL: Optional[str] = "INFO"
    BATCH_SIZE: Optional[PositiveInt] = 100000000
    DROP_DESTINATION_TABLE_IF_EXISTS: Optional[bool] = False
    ON_CLUSTER_DIRECTIVE: Optional[str] = ""
    USE_S3_CLUSTER: Optional[bool] = False

    def get_on_cluster(self):
        if not self.ON_CLUSTER_DIRECTIVE or self.ON_CLUSTER_DIRECTIVE == "":
            return ""
        return f"ON CLUSTER '{self.ON_CLUSTER_DIRECTIVE}'"
