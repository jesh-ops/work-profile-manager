@echo off
cd /d "%~dp0"

set PYTHON_EXE=%~dp0.venv\Scripts\python.exe

if not exist "%PYTHON_EXE%" (
    echo Python virtual environment not found.
    echo Please run: py -3 -m venv .venv
    pause
    exit /b 1
)

echo Starting Work Profile Manager...
start "" http://127.0.0.1:5000
"%PYTHON_EXE%" run.py

if errorlevel 1 (
    echo.
    echo App failed to start. Check the error output above.
    pause
)
