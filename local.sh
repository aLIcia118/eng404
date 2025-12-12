#!/bin/bash

export FLASK_ENV=development
# export PROJ_DIR=$PWD
export PROJ_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export DEBUG=1

# run our server locally:
# PYTHONPATH=$(pwd):$PYTHONPATH
# Directory of this script = project root
PYTHONPATH="$PROJ_DIR:${PYTHONPATH:-}"

export FLASK_APP=server.endpoints

flask run --debug --host=127.0.0.1 --port=8000

# FLASK_APP=server.endpoints flask run --debug --host=127.0.0.1 --port=8000
