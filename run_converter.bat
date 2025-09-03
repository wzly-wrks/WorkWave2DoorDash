@echo off
echo Starting WorkWave to DoorDash Converter...
python workwave_to_doordash.py
if %ERRORLEVEL% NEQ 0 (
    echo Error running converter. Please make sure Python is installed.
    pause
)