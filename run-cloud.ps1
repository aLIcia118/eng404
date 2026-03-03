# Cloud server script
# Sets REACT_APP_API_URL to cloud server and runs frontend dev server

$scriptDir = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
Set-Location "$scriptDir\frontend"

$env:REACT_APP_API_URL = "https://api.eng404.cloud"

Write-Host "Starting frontend with CLOUD server configuration..."
Write-Host "REACT_APP_API_URL: $env:REACT_APP_API_URL"

npm start
