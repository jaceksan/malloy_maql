#!/usr/bin/env bash

echo "-------------------------------------------------"
echo "Load data"
echo "-------------------------------------------------"
./load_faa_postgres.py

echo "-------------------------------------------------"
echo "PUT Gooddata models - bootstrap FAA"
echo "-------------------------------------------------"
./bootstrap_model.py

echo "-------------------------------------------------"
echo "PUT Gooddata models - FAA custom"
echo "-------------------------------------------------"
./put_workspace_faa_custom.py
