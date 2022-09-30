#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

from libs.config import default_workspace_id, default_workspace_name, template_data_source_id
from libs.data_source_config import DataSourceConfig
from libs.sdk_wrapper import GoodDataSdkWrapper
from gooddata_sdk import CatalogWorkspace


sdk_wrapper = GoodDataSdkWrapper()
sdk_wrapper.wait_for_gooddata_is_up()
sdk = sdk_wrapper.sdk

ds_config = DataSourceConfig(default_workspace_id)

print(f"Register data source {ds_config.data_source_id} ...")
sdk.catalog_data_source.create_or_update_data_source(ds_config.data_source)

print(f"Create workspace {default_workspace_id} ...")
sdk.catalog_workspace.create_or_update(CatalogWorkspace(default_workspace_id, default_workspace_name))

print("Scan data source and put its metadata ...")
sdk.catalog_data_source.scan_and_put_pdm(data_source_id=ds_config.data_source_id)
print("Generate logical data model ...")
ldm = sdk.catalog_data_source.generate_logical_model(data_source_id=ds_config.data_source_id)
print("Put logical data model ...")

sdk.catalog_workspace_content.put_declarative_ldm(workspace_id=default_workspace_id, ldm=ldm)

print("Store physical and logical models to local folder")
pdm = sdk.catalog_data_source.get_declarative_pdm(ds_config.data_source_id)
# Store PDM into pg_local folder, no matter what data source id in what GD environment was handled
folder = sdk.catalog_data_source.data_source_folder(data_source_id=template_data_source_id, layout_root_path=Path.cwd())
pdm.store_to_disk(folder)
sdk.catalog_workspace.store_declarative_workspace(default_workspace_id)

print("done")
