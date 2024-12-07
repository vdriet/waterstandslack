#!/bin/bash
set -e
export PYTHONPATH=.
pip list --outdated
pylint *.py
pytest tests
docker build --tag waterstandslack .
