#!/bin/bash
# Cloud server script
# Sets REACT_APP_API_URL to cloud server and runs frontend dev server

cd "$(dirname "$0")"/frontend
export REACT_APP_API_URL=https://api.eng404.cloud

echo "Starting frontend with CLOUD server configuration..."
echo "REACT_APP_API_URL: $REACT_APP_API_URL"

npm start
