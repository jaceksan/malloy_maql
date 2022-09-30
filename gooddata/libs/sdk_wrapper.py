# -*- coding: utf-8 -*-
import os
from typing import Optional
from gooddata_sdk import GoodDataSdk


class GoodDataSdkWrapper:

    def __init__(self):
        kwargs = {}
        if self.override_host:
            kwargs["Host"] = self.override_host
        self.sdk = GoodDataSdk.create(host_=self.host, token_=self.token, **kwargs)

    @property
    def host(self) -> str:
        return os.getenv("TIGER_ENDPOINT", "localhost")

    @property
    def token(self) -> str:
        return os.getenv("TIGER_API_TOKEN", "YWRtaW46Ym9vdHN0cmFwOmFkbWluMTIz")

    @property
    def override_host(self) -> Optional[str]:
        return os.getenv("OVERRIDE_HOST")

    def wait_for_gooddata_is_up(self) -> None:
        # Wait for the GoodData.CN docker image to start up
        print(f"Waiting for {self.host} to be up.", flush=True)
        self.sdk.support.wait_till_available(timeout=600)
        print(f"Host {self.host} is up.", flush=True)
