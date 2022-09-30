#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from pathlib import Path
from fastparquet import ParquetFile
from pandas import DataFrame
import logging
from databases.postgres import PostgresDbConfig, Postgres
from libs.data_source_config import DataSourceConfig
from libs.config import default_workspace_id

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
entities = [
    "aircraft_models", "aircraft", "airports", "carriers", "flights"
]
data_dir = Path("..") / "malloy" / "data"
ddl_dir = Path(".") / "ddl" / default_workspace_id
transform_dir = Path(".") / "transform" / default_workspace_id

ds_config = DataSourceConfig(default_workspace_id)


def get_db_config() -> PostgresDbConfig:
    logging.info(f"Going to connect to {ds_config.db_host}:{ds_config.db_port}/{ds_config.db_name}")
    return PostgresDbConfig(
        db_host=ds_config.db_host,
        db_port=ds_config.db_port,
        db_name=ds_config.db_name,
        db_user=ds_config.db_user,
        db_password=ds_config.db_password,
    )


def read_parquet_file(source_file: Path) -> DataFrame:
    return ParquetFile(str(source_file)).to_pandas()


def parquet_to_csv():
    for entity in entities:
        logging.info(f"Convert {entity}.parquet to {entity}.csv")
        parquet_path = data_dir / f"{entity}.parquet"
        df = read_parquet_file(parquet_path)
        # Malloy demo contains rows violating referential integrity
        if entity == "flights":
            df = df[df["origin"] != "SCE"]
        df.to_csv(
            data_dir / f"{entity}.csv",
            sep=',',
            index=False,
            mode='w',
            lineterminator='\n',
            encoding='utf-8'
        )


def recreate_schema(postgres: Postgres):
    postgres.drop_schema_if_exists(ds_config.db_schema)
    postgres.create_schema_if_not_exists(ds_config.db_schema)
    postgres.set_schema(ds_config.db_schema)


def create_tables(postgres: Postgres):
    for entity in entities:
        with open(ddl_dir / f"{entity}.sql") as fp:
            ddl = fp.read()
        postgres.create_table_if_not_exists(ddl, entity)


def load_files(postgres: Postgres):
    for entity in entities:
        csv_file = data_dir / f"{entity}.csv"
        logging.info(f"Loading file {csv_file} ...")
        postgres.load_file(entity, csv_file, skip_header=True)


def transform(postgres: Postgres):
    with open(transform_dir / f"{default_workspace_id}.sql") as fp:
        file_content = fp.read()
    re_split = re.compile(r'^;$', re.M)
    # Skip empty queries created by split
    queries = [q for q in re_split.split(file_content) if re.search(r'[a-zA-Z]', q)]
    for query in queries:
        report_query = re.sub(r'\n', ' ', query)
        logging.info(f"Executing query >{report_query}<")
        postgres.execute_query(query)


def main():
    logging.info("START")
    db_config = get_db_config()
    postgres = Postgres(db_config)
    try:
        recreate_schema(postgres)
        parquet_to_csv()
        create_tables(postgres)
        load_files(postgres)
        transform(postgres)
    finally:
        postgres.close_connections()
        logging.info("END")


if __name__ == "__main__":
    main()
