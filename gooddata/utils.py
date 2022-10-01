from gooddata_sdk import GoodDataSdk

def pre_cache_insights(sdk: GoodDataSdk):
    workspaces = sdk.catalog_workspace.list_workspaces()
    for workspace in workspaces:
        insights = sdk.insights.get_insights(workspace.id)

        for insight in insights:
            sdk.tables.for_insight(workspace.id, insight)