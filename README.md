# WorkWave to DoorDash Converter

A tool to convert WorkWave Route Manager CSV exports to DoorDash import templates.

## Overview

This tool simplifies the process of converting delivery routes exported from WorkWave Route Manager into the format required for bulk imports into DoorDash. It automates the manual process of copying and formatting data, saving time and reducing errors.

## Features

- Easy-to-use graphical interface
- Automatic parsing of WorkWave CSV files
- Configurable pickup location settings
- Automatic formatting of addresses, names, dates, and times
- Automatic counting of meal items for each client
- Processing of delivery notes to create appropriate dropoff instructions
  - Automatically adds "Please deliver directly to the client. Do not leave unattended unless client has provided a cooler." to all instructions
- Saves output in DoorDash-compatible CSV format

## Requirements

- Python 3.6 or higher
- Required Python packages (installed automatically by setup script):
  - pandas

## Installation

### Windows

1. Make sure Python is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
2. Extract all files from the ZIP archive to a folder on your computer.
3. Run `setup.py` to install required dependencies:
   ```
   python setup.py
   ```
4. Once setup is complete, you can run the converter using the included batch file:
   ```
   run_converter.bat
   ```

### Mac/Linux

1. Make sure Python is installed on your system.
2. Extract all files from the ZIP archive to a folder on your computer.
3. Open Terminal and navigate to the folder containing the extracted files.
4. Make the setup and run scripts executable:
   ```
   chmod +x setup.py run_converter.sh
   ```
5. Run the setup script to install required dependencies:
   ```
   python3 setup.py
   ```
6. Once setup is complete, you can run the converter using the included shell script:
   ```
   ./run_converter.sh
   ```

## Usage

1. Launch the converter using the appropriate script for your operating system.
2. Click "Browse..." to select your WorkWave CSV export file.
3. The output file path will be automatically generated, but you can change it if desired.
4. Configure the pickup settings as needed:
   - Pickup Location ID (default: ANGEL-1)
   - Pickup Location Name (default: PATH Kitchen)
   - Pickup Phone Number (your contact number)
   - Timezone (default: US/Pacific)
   - Pickup Window Start/End times (default: 13:00:00 / 15:00:00)
   - Pickup Instructions (default: Amped kitchens enter and ask for dispatch manager)
   - Default Dropoff Instructions (used when notes are blank)
5. Click "Convert" to process the file.
6. Once conversion is complete, a success message will be displayed.
7. The output CSV file can now be uploaded to DoorDash for bulk order creation.

## Important Notes

- Before processing routes for DoorDash delivery, verify that all addresses are within 15 miles of the pickup location.
- The converter sets "Number of Items" to 1 for all orders, as mentioned in the workflow.
- Special instructions like "Call CS for issues" or "Please deliver after X time" are automatically removed from dropoff instructions.
- For clients at the same address, the converter keeps them as separate orders to make it easier for packers.

## Field Mapping

The tool maps fields from WorkWave to DoorDash as follows:

| DoorDash Field | WorkWave Source |
|----------------|-----------------|
| Pickup Location ID* | Configurable (default: ANGEL-1) |
| Order ID* | Order Number |
| Date of Delivery* | Date (reformatted) |
| Pickup Window Start* | Configurable |
| Pickup Window End* | Configurable |
| Timezone* | Configurable (default: US/Pacific) |
| Client First Name* | Extracted from Name |
| Client Last Name* | Extracted from Name (initial only) |
| Client Street Address* | Extracted from Address |
| Client Unit | Apartment/CompanyName or ApartmentInfo |
| Client City* | Extracted from Address |
| Client State* | Extracted from Address |
| Client ZIP* | Extracted from Address |
| Client Phone* | Phone Number |
| Number of Items* | Always "1" |
| Dropoff Instructions | Notes (processed) |
| Pickup Location Name | Configurable (default: PATH Kitchen) |
| Pickup Phone Number | Configurable |
| Pickup Instructions | Configurable |
| Order Volume | Left blank |

## Troubleshooting

- **Error reading WorkWave CSV**: Make sure the file is a valid CSV export from WorkWave Route Manager.
- **Missing required fields**: Check that your WorkWave export contains all necessary fields.
- **Address parsing issues**: If addresses aren't being parsed correctly, check for unusual formatting in the WorkWave export.
- **Python not found**: Make sure Python is installed and added to your system PATH.

## Support

For issues or questions, please contact the tool developer @ weezly@weezly.works

Made with ❤️ in ~/Los_Angeles by weezly.works & his army of robots. ©2025 under the MIT license
