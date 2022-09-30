#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from libs.config import custom_workspace_id
from libs.sdk_wrapper import GoodDataSdkWrapper

sdk_wrapper = GoodDataSdkWrapper()
sdk_wrapper.wait_for_gooddata_is_up()
sdk = sdk_wrapper.sdk

sdk.catalog_workspace_content.store_declarative_analytics_model(custom_workspace_id)

print("done")
