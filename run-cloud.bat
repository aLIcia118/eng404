@echo off
REM Cloud server script
REM Sets REACT_APP_API_URL to cloud server and runs frontend dev server

cd /d "%~dp0\frontend"
set REACT_APP_API_URL=https://api.eng404.cloud

echo Starting frontend with CLOUD server configuration...
echo REACT_APP_API_URL: %REACT_APP_API_URL%

call npm start
pause
