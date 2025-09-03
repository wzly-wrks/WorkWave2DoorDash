# WorkWave to DoorDash Converter - User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [Using the Converter](#using-the-converter)
5. [Configuration Options](#configuration-options)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)
8. [FAQ](#faq)

## Introduction

The WorkWave to DoorDash Converter is a tool designed to simplify the process of converting delivery routes exported from WorkWave Route Manager into the format required for bulk imports into DoorDash. This tool automates the manual process of copying and formatting data, saving time and reducing errors.

### Key Features

- Easy-to-use graphical interface
- Automatic parsing of WorkWave CSV files
- Configurable pickup location settings
- Automatic formatting of addresses, names, dates, and times
- Processing of delivery notes to create appropriate dropoff instructions
- Saves output in DoorDash-compatible CSV format

## Installation

### Windows

1. Extract all files from the ZIP archive to a folder on your computer.
2. If you received the executable version:
   - Simply run `WorkWave_to_DoorDash_Converter.exe` to start the application.
3. If you received the Python source version:
   - Make sure Python 3.6 or higher is installed on your system.
   - Run `setup.py` to install required dependencies.
   - Use `run_converter.bat` to start the application.

### Mac/Linux

1. Extract all files from the ZIP archive to a folder on your computer.
2. If you received the executable version:
   - Open Terminal and navigate to the folder containing the extracted files.
   - Make the executable file runnable: `chmod +x WorkWave_to_DoorDash_Converter`
   - Run the application: `./WorkWave_to_DoorDash_Converter`
3. If you received the Python source version:
   - Make sure Python 3.6 or higher is installed on your system.
   - Make the setup and run scripts executable: `chmod +x setup.py run_converter.sh`
   - Run the setup script: `python3 setup.py`
   - Start the application: `./run_converter.sh`

## Getting Started

### Before You Begin

Before using the converter, make sure you have:

1. A CSV export from WorkWave Route Manager containing the routes you want to convert.
2. Verified that all addresses in the route are within 15 miles of your pickup location (as required by DoorDash).

### Exporting Routes from WorkWave

To export routes from WorkWave Route Manager:

1. Log in to WorkWave Route Manager.
2. Navigate to "Route Optimization History".
3. Find the date of the route you want to export.
4. Click "View Info" and then "Get Routes".
5. Export the route as a CSV file.

## Using the Converter

### Step 1: Launch the Application

Run the converter application using the appropriate method for your operating system (see Installation section).

### Step 2: Select Input File

1. Click the "Browse..." button next to "WorkWave CSV File".
2. Navigate to and select your WorkWave CSV export file.
3. The output file path will be automatically generated based on the input file name.

### Step 3: Configure Settings

Adjust the settings as needed:

- **Pickup Location ID**: Default is "ANGEL-1" (as mentioned in the training video).
- **Pickup Location Name**: Default is "PATH Kitchen".
- **Pickup Phone Number**: Enter the phone number that DoorDash drivers should call when they arrive for pickup.
- **Timezone**: Default is "US/Pacific".
- **Pickup Window Start/End**: Set the time window for pickups (default is 13:00:00 to 15:00:00).
- **Pickup Instructions**: Instructions for the driver when they arrive at the pickup location.
- **Default Dropoff Instructions**: Instructions used when a client has no specific delivery notes.

The converter will automatically count the number of meal items for each client by looking at the meal-related fields in the WorkWave CSV (fields that start with "lb|"). This count will be used for the "Number of Items" field in the DoorDash template.

### Step 4: Convert

1. Click the "Convert" button to process the file.
2. A progress indicator will show the conversion status.
3. Once complete, a success message will display the number of orders processed.

### Step 5: Upload to DoorDash

1. Log in to your DoorDash merchant account.
2. Navigate to "Orders" and select "Bulk Order".
3. Click "Upload CSV" and select the converted CSV file.
4. Follow the DoorDash prompts to complete the bulk order submission.

## Configuration Options

### Pickup Settings

- **Pickup Location ID**: A unique identifier for your pickup location. Always use "ANGEL-1" unless instructed otherwise.
- **Pickup Location Name**: The name of your pickup location that will appear to DoorDash drivers.
- **Pickup Phone Number**: The contact number for drivers when they arrive for pickup.
- **Timezone**: The timezone for your delivery schedule (e.g., "US/Pacific", "US/Eastern").
- **Pickup Window Start/End**: The time window during which drivers should pick up orders.
- **Pickup Instructions**: Specific instructions for drivers when they arrive at the pickup location.

### Delivery Settings

- **Default Dropoff Instructions**: Instructions used when a client has no specific delivery notes in WorkWave.

**Important**: The standard note "Please deliver directly to the client. Do not leave unattended unless client has provided a cooler." will be automatically added to all delivery instructions.

## Best Practices

### Organizing Your Files

- Create a dedicated folder for your DoorDash conversions.
- Save converted files with descriptive names that include the route and date.
- Keep a backup of your original WorkWave exports.

### Reusing Previous Conversions

As mentioned in the training video, you can save time by:

1. Keeping previous DoorDash CSV files for routes that are regularly scheduled.
2. When the same route needs to be scheduled again:
   - Open the previous CSV file
   - Update the delivery date and pickup window times
   - Keep existing clients that are still on the route
   - Remove clients that are no longer on the route
   - Add new clients to the route
   - Save as a new CSV file

### Verifying Address Distance

Before processing routes for DoorDash delivery:

1. Check that all addresses are within 15 miles of the pickup location.
2. You can use Google Maps to verify distances:
   - Enter the pickup location address
   - Get directions to the client address
   - Check that the distance is under 15 miles

## Troubleshooting

### Common Issues

#### "Error reading WorkWave CSV file"
- Make sure the file is a valid CSV export from WorkWave Route Manager.
- Check that the file is not open in another program.
- Try re-exporting the file from WorkWave.

#### "Missing required fields"
- Ensure your WorkWave export contains all necessary fields.
- The converter requires fields like Address, Name, Phone Number, etc.

#### "Address parsing issues"
- If addresses aren't being parsed correctly, check for unusual formatting in the WorkWave export.
- You may need to manually edit addresses with unusual formats.

#### "Python not found" (source version only)
- Make sure Python is installed and added to your system PATH.
- Try running the setup script again.

### Getting Help

If you encounter issues not covered in this guide, please contact the tool developer for assistance.

## FAQ

### Q: Can I edit the CSV file after conversion?
A: Yes, you can open the converted CSV file in Excel or any spreadsheet program to make manual adjustments before uploading to DoorDash.

### Q: How do I handle clients at the same address?
A: As mentioned in the training video, keep them as separate orders to make it easier for packers, even though you'll be paying for two deliveries.

### Q: What if a client has special delivery instructions?
A: The converter automatically processes delivery notes from WorkWave, removing irrelevant instructions like "Call CS for issues" and preserving important details.

### Q: How do I update the pickup location?
A: You can change the pickup location details in the settings section of the converter before processing the file.

### Q: Can I save my configuration settings for future use?
A: The current version does not save settings between sessions. You'll need to re-enter your preferred settings each time you run the application.