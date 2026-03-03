# Local development server script
# Sets REACT_APP_API_URL to local server and runs frontend dev server

$scriptDir = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
Set-Location "$scriptDir\frontend"

$env:REACT_APP_API_URL = "http://localhost:8000"

Write-Host "Starting frontend with LOCAL server configuration..."
Write-Host "REACT_APP_API_URL: $env:REACT_APP_API_URL"

npm start
