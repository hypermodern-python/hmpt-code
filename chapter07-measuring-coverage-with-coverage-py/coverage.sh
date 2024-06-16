#!/bin/bash

set -euo pipefail

# Test under Python 3.7
uv venv -p 3.7
uv pip sync py37-dev-requirements.txt
uv pip install -e . --no-deps
echo 'import coverage; coverage.process_startup()' > .venv/lib/python3.7/site-packages/_coverage.pth
py -m coverage run -m pytest -v

# Test under Python 3.12
uv venv -p 3.12
uv pip sync dev-requirements.txt
uv pip install -e . --no-deps
echo 'import coverage; coverage.process_startup()' > .venv/lib/python3.12/site-packages/_coverage.pth
py -m coverage run -m pytest -v

# Report
py -m coverage combine
py -m coverage report
