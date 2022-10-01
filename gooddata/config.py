import os

from gooddata_sdk import GoodDataSdk

class Config:
    __host = os.environ["TIGER_HOST"]
    __token = os.environ["TIGER_TOKEN"]
    sdk = GoodDataSdk.create(host_=__host, token_=__token)

