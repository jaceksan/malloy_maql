# -*- coding: utf-8 -*-
import os
from gooddata_sdk import CatalogDataSource, BasicCredentials


class DataSourceConfig:
    # Default values correspond to the GoodData community edition running on localhost (docker-compose.yaml)
    def __init__(self, workspace_id: str):
        self.workspace_id = workspace_id

    @property
    def db_host(self) -> str:
        return os.getenv('DB_HOST', 'localhost')

    @property
    def db_port(self) -> int:
        return int(os.getenv('DB_PORT', 5432))

    @property
    def db_name(self) -> str:
        return os.getenv('DB_NAME', 'demo')

    @property
    def db_user(self) -> str:
        return os.getenv('DB_USER', 'demouser')

    @property
    def db_password(self) -> str:
        return os.getenv('DB_PASSWORD', 'demopass')

    @property
    def db_jdbc_url(self) -> str:
        return f"jdbc:postgresql://{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def db_schema(self) -> str:
        return os.getenv("DB_SCHEMA", self.workspace_id)

    @property
    def data_source_id(self) -> str:
        return os.getenv("DATA_SOURCE_ID", "postgres_local")

    @property
    def data_source_name(self) -> str:
        return os.getenv("DATA_SOURCE_NAME", "Postgres local")

    @property
    def data_source(self):
        return CatalogDataSource(
            id=self.data_source_id,
            name=self.data_source_name,
            schema=self.db_schema,
            credentials=BasicCredentials(
                username=self.db_user, password=self.db_password
            ),
            url=self.db_jdbc_url,
            data_source_type="POSTGRESQL"
        )
