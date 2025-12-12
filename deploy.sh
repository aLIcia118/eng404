#!/bin/bash
# This script deploys the ENG404 Flask app to PythonAnywhere.
# Usage:
#   export ENG404_PA_PWD=your_pythonanywhere_password
#   ./deploy.sh

set -e

readonly PROJ_NAME=eng404
readonly PROJ_DIR=$PROJ_NAME
readonly VENV=$PROJ_NAME
readonly PA_DOMAIN="rachelchen.pythonanywhere.com"
readonly PA_USER="rachelchen"

echo "Project directory : $PROJ_DIR"
echo "PythonAnywhere user: $PA_USER"
echo "PythonAnywhere site: $PA_DOMAIN"
echo "Virtual environment: $VENV"

# Check required environment variable
if [ -z "$ENG404_PA_PWD" ]; then
    echo "ERROR: ENG404_PA_PWD environment variable is not set." >&2
    exit 1
fi

echo "PythonAnywhere password is set"
echo "Starting deployment..."

sshpass -p "$ENG404_PA_PWD" ssh \
    -o BatchMode=yes \
    -o StrictHostKeyChecking=no \
    "$PA_USER"@ssh.pythonanywhere.com << EOF
cd ~/$PROJ_DIR
PA_USER=$PA_USER PROJ_DIR=~/$PROJ_DIR VENV=$VENV PA_DOMAIN=$PA_DOMAIN ./rebuild.sh
EOF

echo "Deployment completed successfully."
