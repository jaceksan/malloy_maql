#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (C) 2020 GoodData Corporation
from __future__ import annotations

import logging
import traceback
from time import time, sleep
from typing import Any
from pathlib import Path
import attr
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import errors, errorcodes


CONNECTION_TIMEOUT = 60000  # milliseconds


@attr.s(auto_attribs=True, kw_only=True)
class PostgresDbConfig:
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str


class Postgres:
    def __init__(self, db_config: PostgresDbConfig):
        self._db_config = db_config
        self._conn = self.get_connection_timeout()
        self._cur = self._conn.cursor()

    def get_connection(self) -> Any:
        logging.debug("Connecting to POSTGRES/REDSHIFT - {}@{}:{}/{}".format(
            self._db_config.db_user,
            self._db_config.db_host,
            self._db_config.db_port,
            self._db_config.db_name
        ))
        conn = psycopg2.connect(
            user=self._db_config.db_user,
            password=self._db_config.db_password,
            host=self._db_config.db_host,
            port=self._db_config.db_port,
            database=self._db_config.db_name
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return conn

    def get_connection_timeout(self, timeout: int = CONNECTION_TIMEOUT) -> Any:
        start = time()
        duration = 0
        err_message = ''
        exception = ''
        while duration < timeout:
            try:
                return self.get_connection()
            except Exception as e:
                err_message = str(e).split("\n")[0]
                duration = int((time() - start)*1000)
                exception = traceback.format_exc()
                sleep(1)
        # If timeout is reached, print last error message and exception and interrupt processing
        raise Exception(
            'Cannot connect to database, timeout reached, interrupt processing.\n' +
            f'db={self._db_config.db_name}, duration={duration} err={err_message}\n' +
            f'exception: {exception}'

        )

    def close_connections(self) -> None:
        if self._conn:
            self._conn.close()

    def execute_query(self, query: str) -> None:
        self._cur.execute(query)

    def drop_schema_if_exists(self, schema_name: str) -> None:
        self.execute_query(f"DROP SCHEMA IF EXISTS {schema_name} CASCADE")

    def create_schema_if_not_exists(self, schema_name: str) -> None:
        self.execute_query(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")

    def set_schema(self, schema_name: str) -> None:
        self.execute_query(f"SET SEARCH_PATH TO {schema_name}")

    @classmethod
    def is_recoverable(cls, e: Exception) -> bool:
        """
        Determines whether exception may be temporary within the context of db driver
        """
        return isinstance(e, (errors.UndefinedTable,))

    def create_table_if_not_exists(self, sql_stmt: str, table_name: str) -> bool:
        table_created = False
        try:
            self.execute_query(sql_stmt)
            table_created = True
        except errors.lookup(errorcodes.DUPLICATE_TABLE):
            logging.info(f'skip creating table {table_name}, it has already been created')

        return table_created

    def load_file(self, table_name: str, file: Path, skip_header: bool) -> None:
        skip_header_directive = ""
        if skip_header:
            skip_header_directive = ', HEADER'
        stmt = f"""
            COPY {table_name} FROM STDIN
            ( FORMAT csv, DELIMITER ','{skip_header_directive}, QUOTE '"', ESCAPE '\\')
        """
        with open(file) as fp:
            self._cur.copy_expert(stmt, fp)
