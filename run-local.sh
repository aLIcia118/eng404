#!/bin/bash
# Local development server script
# Sets REACT_APP_API_URL to local server and runs frontend dev server

cd "$(dirname "$0")"/frontend
export REACT_APP_API_URL=http://localhost:8000

echo "Starting frontend with LOCAL server configuration..."
echo "REACT_APP_API_URL: $REACT_APP_API_URL"

npm start
