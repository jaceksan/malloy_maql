#!/usr/bin/env bash

echo "-------------------------------------------------"
echo "Load data"
echo "-------------------------------------------------"
./load_faa_postgres.py

echo "-------------------------------------------------"
echo "Transform data"
echo "-------------------------------------------------"
pushd transform || return
dbt deps
dbt run --profiles-dir profile --target dev
dbt test --profiles-dir profile --target dev
popd || return

echo "-------------------------------------------------"
echo "PUT Gooddata models - bootstrap FAA workspace"
echo "-------------------------------------------------"
./bootstrap_model.py

echo "-------------------------------------------------"
echo "PUT Gooddata models - FAA custom workspace"
echo "-------------------------------------------------"
./put_workspace_faa_custom.py
