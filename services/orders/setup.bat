@echo off
REM Setup script for Data Analytics Microservice (Windows)

echo Setting up Data Analytics Microservice...

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Create necessary directories
echo Creating necessary directories...
if not exist "uploads" mkdir uploads
if not exist "logs" mkdir logs
if not exist "temp" mkdir temp
if not exist "reports" mkdir reports

echo Setup completed successfully!
echo.
echo To run the service:
echo 1. Activate virtual environment:
echo    venv\Scripts\activate.bat
echo 2. Run the application:
echo    python app.py
echo.
echo The service will be available at: http://localhost:5000
pause
