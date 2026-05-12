@echo off
REM ZORQ AI Chatbot - Quick Start for Windows (Python Edition)

echo.
echo ╔════════════════════════════════════╗
echo ║   ZORQ AI Chatbot - Setup Script   ║
echo ║   Windows + Python Edition         ║
echo ╚════════════════════════════════════╝
echo.

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python is not installed!
    echo Please download and install Python from: https://www.python.org/
    echo Make sure to CHECK "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

echo ✅ Python found:
python --version
echo.

REM Install dependencies
echo 📦 Installing Python dependencies...
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed!
echo.

REM Start the server
echo 🚀 Starting ZORQ server...
echo.
echo Server will run on: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python server.py

