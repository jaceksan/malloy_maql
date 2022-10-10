#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from libs.constants import custom_workspace_id
from libs.sdk_wrapper import GoodDataSdkWrapper

sdk = GoodDataSdkWrapper().sdk

sdk.catalog_workspace_content.store_declarative_analytics_model(custom_workspace_id)

print("done")
