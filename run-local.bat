@echo off
REM Local development server script
REM Sets REACT_APP_API_URL to local server and runs frontend dev server

cd /d "%~dp0\frontend"
set REACT_APP_API_URL=http://localhost:8000

echo Starting frontend with LOCAL server configuration...
echo REACT_APP_API_URL: %REACT_APP_API_URL%

call npm start
pause
