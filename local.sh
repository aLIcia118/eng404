#!/bin/bash

export FLASK_ENV=development
export PROJ_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export DEBUG=1

# run our server locally:
PYTHONPATH="$PROJ_DIR:${PYTHONPATH:-}"

export FLASK_APP=server.endpoints

flask run --debug --host=127.0.0.1 --port=8000
