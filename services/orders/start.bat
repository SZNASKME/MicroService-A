@echo off
REM Production startup script for Data Analytics Microservice (Windows)

echo 🚀 Starting Data Analytics Microservice...

REM Load environment variables
if exist ".env.production" (
    echo 📦 Loading production environment...
    for /f "usebackq tokens=1,2 delims==" %%a in (".env.production") do (
        if not "%%a"=="" if not "%%a:~0,1%%"=="#" set %%a=%%b
    )
)

REM Create required directories
echo 📁 Creating required directories...
if not exist "logs" mkdir logs
if not exist "uploads" mkdir uploads

REM Install/update dependencies
echo 📋 Installing dependencies...
pip install --no-cache-dir -r requirements.txt

REM Start the application with Gunicorn
echo 🌟 Starting application with Gunicorn...
gunicorn ^
    --bind 0.0.0.0:%PORT% ^
    --workers %WORKERS% ^
    --worker-class sync ^
    --worker-connections %WORKER_CONNECTIONS% ^
    --max-requests %MAX_REQUESTS% ^
    --max-requests-jitter %MAX_REQUESTS_JITTER% ^
    --timeout %TIMEOUT% ^
    --keep-alive %KEEP_ALIVE% ^
    --access-logfile logs/access.log ^
    --error-logfile logs/error.log ^
    --log-level %LOG_LEVEL% ^
    --capture-output ^
    wsgi:application

REM Set default values if not set
if not defined PORT set PORT=5000
if not defined WORKERS set WORKERS=4
if not defined WORKER_CONNECTIONS set WORKER_CONNECTIONS=1000
if not defined MAX_REQUESTS set MAX_REQUESTS=1000
if not defined MAX_REQUESTS_JITTER set MAX_REQUESTS_JITTER=100
if not defined TIMEOUT set TIMEOUT=30
if not defined KEEP_ALIVE set KEEP_ALIVE=2
if not defined LOG_LEVEL set LOG_LEVEL=warning
