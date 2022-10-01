#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from config import Config

sdk = Config.sdk

print("Load and put data sources ...")
sdk.catalog_data_source.store_declarative_data_sources()
print("Load and put workspaces ...")
sdk.catalog_workspace.store_declarative_workspaces()

print("done")
