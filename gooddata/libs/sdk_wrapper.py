# -*- coding: utf-8 -*-
import os
from typing import Optional
from gooddata_sdk import GoodDataSdk


class GoodDataSdkWrapper:

    def __init__(self, timeout=600):
        kwargs = {}
        if self.override_host:
            kwargs["Host"] = self.override_host
        self.sdk = GoodDataSdk.create(host_=self.host, token_=self.token, **kwargs)
        self.wait_for_gooddata_is_up(timeout)

    @property
    def host(self) -> str:
        return os.getenv("TIGER_ENDPOINT", "localhost")

    @property
    def token(self) -> str:
        return os.getenv("TIGER_API_TOKEN", "YWRtaW46Ym9vdHN0cmFwOmFkbWluMTIz")

    @property
    def override_host(self) -> Optional[str]:
        return os.getenv("OVERRIDE_HOST")

    def wait_for_gooddata_is_up(self, timeout) -> None:
        # Wait for the GoodData.CN docker image to start up
        print(f"Waiting for {self.host} to be up.", flush=True)
        self.sdk.support.wait_till_available(timeout=timeout)
        print(f"Host {self.host} is up.", flush=True)

    def pre_cache_insights(self, workspaces: list = None) -> None:
        if not workspaces:
            workspaces = [w.id for w in self.sdk.catalog_workspace.list_workspaces()]
        for workspace_id in workspaces:
            insights = self.sdk.insights.get_insights(workspace_id)

            for insight in insights:
                self.sdk.tables.for_insight(workspace_id, insight)
