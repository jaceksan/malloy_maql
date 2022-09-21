#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import os
from gooddata_sdk import GoodDataSdk

host = os.environ["TIGER_ENDPOINT"]
token = os.environ["TIGER_API_TOKEN"]

sdk = GoodDataSdk.create(host, token)

print("Load and put data sources ...")
sdk.catalog_data_source.load_and_put_declarative_data_sources(credentials_path=Path("data_sources_credentials.yaml"))
print("Load and put workspaces ...")
sdk.catalog_workspace.load_and_put_declarative_workspaces()

print("done")
