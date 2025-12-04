#!/bin/bash
# This shell script deploys a new version of the ENG404 app to PythonAnywhere.

PROJ_NAME=eng404

PROJ_DIR=$PROJ_NAME
VENV=$PROJ_NAME
PA_DOMAIN="rachelchen.pythonanywhere.com"
PA_USER="rachelchen"

echo "Project dir = $PROJ_DIR"
echo "PA domain = $PA_DOMAIN"
echo "Virtual env = $VENV"

# Expect the PythonAnywhere password in ENG404_PA_PWD
if [ -z "$ENG404_PA_PWD" ]
then
    echo "The PythonAnywhere password var (ENG404_PA_PWD) must be set in the env."
    exit 1
fi

echo "PA user = $PA_USER"
echo "PA password = $ENG404_PA_PWD"

echo "SSHing to PythonAnywhere."
sshpass -p "$ENG404_PA_PWD" ssh -o "StrictHostKeyChecking no" "$PA_USER"@ssh.pythonanywhere.com << EOF
    cd ~/$PROJ_DIR; PA_USER=$PA_USER PROJ_DIR=~/$PROJ_DIR VENV=$VENV PA_DOMAIN=$PA_DOMAIN ./rebuild.sh
EOF
