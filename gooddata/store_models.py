#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from gooddata_sdk import GoodDataSdk

host = os.environ["TIGER_ENDPOINT"]
token = os.environ["TIGER_API_TOKEN"]

sdk = GoodDataSdk.create(host, token)

print("Load and put data sources ...")
sdk.catalog_data_source.store_declarative_data_sources()
print("Load and put workspaces ...")
sdk.catalog_workspace.store_declarative_workspaces()

print("done")
