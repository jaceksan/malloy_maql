#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gooddata_sdk import GoodDataSdk
import os
from pathlib import Path

host = os.environ["TIGER_ENDPOINT"]
token = os.environ["TIGER_API_TOKEN"]
data_source_id = "postgres_local"
workspace_id = "faa"

sdk = GoodDataSdk.create(host, token)

print("Load and put(register) data sources ...")
sdk.catalog_data_source.load_and_put_declarative_data_sources(credentials_path=Path("data_sources_credentials.yaml"))
print("Load and put declarative workspaces ...")
sdk.catalog_workspace.load_and_put_declarative_workspace(workspace_id=workspace_id)
print("Scan data source and put its metadata ...")
sdk.catalog_data_source.scan_and_put_pdm(data_source_id=data_source_id)
print("Generate logical data model ...")
ldm = sdk.catalog_data_source.generate_logical_model(data_source_id=data_source_id)
print("Put logical data model ...")
sdk.catalog_workspace_content.put_declarative_ldm(workspace_id=workspace_id, ldm=ldm)
print("Store physical and logical models to local folder")
sdk.catalog_data_source.store_declarative_data_sources()
sdk.catalog_workspace.store_declarative_workspaces()

print("done")
