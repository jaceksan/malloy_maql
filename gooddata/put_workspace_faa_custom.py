#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (C) 2022 GoodData Corporation
from libs.constants import custom_workspace_id, custom_workspace_name, template_data_source_id
from libs.data_source_config import DataSourceConfig
from libs.sdk_wrapper import GoodDataSdkWrapper
from gooddata_sdk import CatalogWorkspace


sdk_wrapper = GoodDataSdkWrapper()
sdk = sdk_wrapper.sdk

ds_config = DataSourceConfig(custom_workspace_id)

print(f"Create or update workspace {custom_workspace_id} ...")
sdk.catalog_workspace.create_or_update(
    CatalogWorkspace(workspace_id=custom_workspace_id, name=custom_workspace_name)
)

print(f"Put LDM ...")
ldm = sdk.catalog_workspace_content.load_declarative_ldm(workspace_id=custom_workspace_id)
# Replace default data source id in LDM with the requested data source id
if template_data_source_id != ds_config.data_source_id:
    print(f"Mapping data source {template_data_source_id} to {ds_config.data_source_id}")
    data_source_mapping = {template_data_source_id: ds_config.data_source_id}
    ldm.modify_mapped_data_source(data_source_mapping)
sdk.catalog_workspace_content.put_declarative_ldm(workspace_id=custom_workspace_id, ldm=ldm)

print(f"Put ADM ...")
sdk.catalog_workspace_content.load_and_put_declarative_analytics_model(workspace_id=custom_workspace_id)

print("Pre-cache insights ...")
sdk_wrapper.pre_cache_insights([custom_workspace_id])

print("done")
