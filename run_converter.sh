#!/bin/bash
echo "Starting WorkWave to DoorDash Converter..."
python3 workwave_to_doordash.py
if [ $? -ne 0 ]; then
    echo "Error running converter. Please make sure Python is installed."
    read -p "Press Enter to continue..."
fi