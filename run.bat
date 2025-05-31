@echo off
title Flask Application Server
echo Starting Flask Application...

REM Change to application directory
cd /d %~dp0

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Set environment variables
set FLASK_APP=app.py
set FLASK_ENV=production

REM Start the server using waitress
echo Starting production server...
start /b pythonw -c "from waitress import serve; from app import app; serve(app, host='0.0.0.0', port=5000, url_scheme='http')" > nul 2>&1

REM If server crashes, show error and wait
if errorlevel 1 (
    echo.
    echo Error occurred! Check the error message above.
    pause
)
