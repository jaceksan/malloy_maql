#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import os
from gooddata_sdk import GoodDataSdk

host = os.environ["TIGER_ENDPOINT"]
token = os.environ["TIGER_API_TOKEN"]

sdk = GoodDataSdk.create(host, token, Host="localhost")

# Wait for the GoodData.CN docker image to start up
print(f"Waiting for {host} to be up.", flush=True)
sdk.support.wait_till_available(timeout=600)
print(f"Host {host} is up.", flush=True)

print("Load and put data sources ...")
sdk.catalog_data_source.load_and_put_declarative_data_sources(credentials_path=Path("data_sources_credentials.yaml"))
print("Load and put workspaces ...")
sdk.catalog_workspace.load_and_put_declarative_workspaces()

print("done")
