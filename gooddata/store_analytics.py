#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from config import Config

sdk = Config.sdk
workspace_id = "faa_simple"

sdk.catalog_workspace_content.store_declarative_analytics_model(workspace_id)

print("done")
