#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gooddata_sdk import GoodDataSdk
import os

host = os.environ["TIGER_ENDPOINT"]
token = os.environ["TIGER_API_TOKEN"]
workspace_id = "faa_simple"

sdk = GoodDataSdk.create(host, token)

sdk.catalog_workspace_content.store_declarative_analytics_model(workspace_id)

print("done")
