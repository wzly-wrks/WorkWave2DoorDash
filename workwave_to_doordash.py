import csv
import re
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime
import pandas as pd

class WorkWaveToDoorDashConverter:
    """
    Tool to convert WorkWave Route Manager CSV exports to DoorDash import templates.
    """
    
    def __init__(self):
        """Initialize the converter with default settings."""
        # Default settings
        self.pickup_location_id = "ANGEL-1"
        self.pickup_location_name = "PATH Kitchen"
        self.pickup_phone_number = ""  # Will be configurable in the UI
        self.pickup_instructions = "Amped kitchens enter and ask for dispatch manager"
        self.pickup_window_start = "13:00:00"
        self.pickup_window_end = "15:00:00"
        self.timezone = "US/Pacific"
        self.default_dropoff_instructions = "Please call upon arrival and hand meals to client. Please deliver directly to the client. Do not leave unattended unless client has provided a cooler."
        
        # Field mappings
        self.workwave_fields = {
            'address': 'Address',
            'unit': 'Apartment/CompanyName',
            'unit_info': 'ApartmentInfo',
            'date': 'Date',
            'order_number': 'Order Number',
            'name': 'Name',
            'notes': 'Notes',
            'phone': 'Phone Number',
            'time_window_start': 'Time Window Start',
            'time_window_end': 'Time Window End'
        }
        
        # DoorDash template fields
        self.doordash_fields = [
            'Pickup Location ID*', 'Order ID*', 'Date of Delivery*', 
            'Pickup Window Start*', 'Pickup Window End*', 'Timezone*',
            'Client First Name*', 'Client Last Name*', 'Client Street Address*',
            'Client Unit', 'Client City*', 'Client State*', 'Client ZIP*',
            'Client Phone*', 'Number of Items*', 'Dropoff Instructions (250 character max)',
            'Pickup Location Name', 'Pickup Phone Number', 'Pickup Instructions', 'Order Volume'
        ]
    
    def parse_address(self, address):
        """
        Parse a WorkWave address into components: street address, city, state, zip.
        Example: "123 Main St, Los Angeles, CA 90001" -> 
                 ("123 Main St", "Los Angeles", "CA", "90001")
        """
        if not address or address.strip() == "":
            return "", "", "", ""
            
        # Remove quotes if present
        address = address.strip('"')
        
        # Try to match the pattern: street, city, state zip
        pattern = r"(.*?),\s*(.*?),\s*([A-Z]{2})\s*(\d{5}(?:-\d{4})?)"
        match = re.search(pattern, address)
        
        if match:
            street = match.group(1).strip()
            city = match.group(2).strip()
            state = match.group(3).strip()
            zip_code = match.group(4).strip()
            return street, city, state, zip_code
        
        # If the pattern doesn't match, try a simpler approach
        parts = address.split(',')
        if len(parts) >= 3:
            street = parts[0].strip()
            city = parts[1].strip()
            state_zip = parts[2].strip().split()
            if len(state_zip) >= 2:
                state = state_zip[0].strip()
                zip_code = state_zip[1].strip()
                return street, city, state, zip_code
        
        # If all else fails, return the original address as street and empty for others
        return address, "", "", ""
    
    def parse_name(self, name):
        """
        Parse a name into first name and last initial.
        Example: "John Doe" -> ("John", "D")
        """
        if not name or name.strip() == "":
            return "", ""
            
        parts = name.strip().split()
        if len(parts) == 1:
            return parts[0], ""
        elif len(parts) > 1:
            first_name = parts[0]
            last_name = parts[-1]
            last_initial = last_name[0] if last_name else ""
            return first_name, last_initial
        else:
            return "", ""
    
    def format_date(self, date_str):
        """
        Convert date from MM/DD/YYYY to YYYY-MM-DD.
        Example: "09/02/2025" -> "2025-09-02"
        """
        if not date_str or date_str.strip() == "":
            return ""
            
        try:
            date_obj = datetime.strptime(date_str, "%m/%d/%Y")
            return date_obj.strftime("%Y-%m-%d")
        except ValueError:
            return date_str
    
    def format_time(self, time_str):
        """
        Convert time from "HH:MM AM/PM" to 24-hour format "HH:MM:SS".
        Example: "07:15 AM" -> "07:15:00"
        """
        if not time_str or time_str.strip() == "":
            return ""
            
        try:
            time_obj = datetime.strptime(time_str, "%I:%M %p")
            return time_obj.strftime("%H:%M:%S")
        except ValueError:
            return time_str
    
    def process_dropoff_instructions(self, notes):
        """
        Process delivery notes to create appropriate dropoff instructions.
        - Remove references to "Call CS for issues"
        - Remove "Please deliver after X time"
        - Add standard delivery instruction to every note
        - If blank, use default instructions
        """
        if not notes or notes.strip() == "":
            return self.default_dropoff_instructions
            
        # Remove quotes if present
        notes = notes.strip('"')
        
        # Remove specific phrases
        notes = re.sub(r"Call CS for (any )?issues\.?", "", notes, flags=re.IGNORECASE)
        notes = re.sub(r"Please deliver after \d+(\:\d+)?( [AP]M)?\.?", "", notes, flags=re.IGNORECASE)
        
        # Clean up any double spaces or leading/trailing spaces
        notes = re.sub(r"\s+", " ", notes).strip()
        
        # If notes are now empty, use default
        if not notes:
            notes = self.default_dropoff_instructions
            
        # Add standard delivery instruction to every note
        standard_note = "Please deliver directly to the client. Do not leave unattended unless client has provided a cooler."
        
        # Check if the standard note is already included in the instructions
        if standard_note.lower() not in notes.lower():
            # Combine notes with standard instruction
            combined_notes = f"{notes} {standard_note}"
            
            # Ensure notes don't exceed 250 characters
            if len(combined_notes) > 250:
                # If too long, prioritize the standard note and truncate the original notes
                max_original_length = 250 - len(standard_note) - 4  # 4 chars for " ..."
                notes = f"{notes[:max_original_length]}... {standard_note}"
            else:
                notes = combined_notes
        
        return notes
    
    def count_meal_items(self, row):
        """
        Count the number of meal items for a client.
        Meal items in WorkWave start with 'lb|'.
        """
        meal_count = 0
        
        # Iterate through all columns in the row
        for key, value in row.items():
            # Check if the column name starts with 'lb|' and has a non-empty value
            if key.startswith('lb|') and value and value.strip():
                try:
                    # Try to convert the value to an integer
                    item_count = int(value.strip())
                    meal_count += item_count
                except ValueError:
                    # If the value is not a number but not empty, count it as 1
                    if value.strip() != "":
                        meal_count += 1
        
        # If no meals were found, default to 1 as mentioned in the transcript
        return max(1, meal_count)
    
    def convert_workwave_to_doordash(self, workwave_data):
        """
        Convert WorkWave data to DoorDash format.
        """
        doordash_data = []
        
        for row in workwave_data:
            # Skip header row or empty rows
            if row.get(self.workwave_fields['address']) == 'Address' or not row.get(self.workwave_fields['address']):
                continue
                
            # Skip departure rows
            if row.get('Type', '').lower() == 'departure':
                continue
                
            # Parse address
            address = row.get(self.workwave_fields['address'], '')
            street, city, state, zip_code = self.parse_address(address)
            
            # Parse name
            name = row.get(self.workwave_fields['name'], '')
            first_name, last_initial = self.parse_name(name)
            
            # Get unit/apartment info
            unit = row.get(self.workwave_fields['unit'], '') or row.get(self.workwave_fields['unit_info'], '')
            
            # Format date
            date_str = row.get(self.workwave_fields['date'], '')
            formatted_date = self.format_date(date_str)
            
            # Process notes/instructions
            notes = row.get(self.workwave_fields['notes'], '')
            dropoff_instructions = self.process_dropoff_instructions(notes)
            
            # Get phone number
            phone = row.get(self.workwave_fields['phone'], '')
            
            # Get order number
            order_id = row.get(self.workwave_fields['order_number'], '')
            
            # Count meal items
            num_items = str(self.count_meal_items(row))
            
            # Create DoorDash row
            doordash_row = {
                'Pickup Location ID*': self.pickup_location_id,
                'Order ID*': order_id,
                'Date of Delivery*': formatted_date,
                'Pickup Window Start*': self.pickup_window_start,
                'Pickup Window End*': self.pickup_window_end,
                'Timezone*': self.timezone,
                'Client First Name*': first_name,
                'Client Last Name*': last_initial,
                'Client Street Address*': street,
                'Client Unit': unit,
                'Client City*': city,
                'Client State*': state,
                'Client ZIP*': zip_code,
                'Client Phone*': phone,
                'Number of Items*': num_items,
                'Dropoff Instructions (250 character max)': dropoff_instructions,
                'Pickup Location Name': self.pickup_location_name,
                'Pickup Phone Number': self.pickup_phone_number,
                'Pickup Instructions': self.pickup_instructions,
                'Order Volume': ''
            }
            
            doordash_data.append(doordash_row)
            
        return doordash_data
    
    def read_workwave_csv(self, file_path):
        """
        Read WorkWave CSV file and return data as a list of dictionaries.
        """
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except Exception as e:
            raise Exception(f"Error reading WorkWave CSV file: {str(e)}")
    
    def write_doordash_csv(self, data, file_path):
        """
        Write DoorDash data to CSV file.
        """
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.doordash_fields)
                writer.writeheader()
                writer.writerows(data)
        except Exception as e:
            raise Exception(f"Error writing DoorDash CSV file: {str(e)}")
    
    def convert_file(self, input_file, output_file):
        """
        Convert WorkWave CSV file to DoorDash CSV file.
        """
        try:
            # Read WorkWave data
            workwave_data = self.read_workwave_csv(input_file)
            
            # Convert to DoorDash format
            doordash_data = self.convert_workwave_to_doordash(workwave_data)
            
            # Write DoorDash data
            self.write_doordash_csv(doordash_data, output_file)
            
            return len(doordash_data)
        except Exception as e:
            raise Exception(f"Conversion error: {str(e)}")


class ConverterGUI:
    """
    GUI for the WorkWave to DoorDash converter.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("WorkWave to DoorDash Converter")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        self.converter = WorkWaveToDoorDashConverter()
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create the GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="WorkWave to DoorDash Converter", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # File selection frame
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="10")
        file_frame.pack(fill=tk.X, pady=10)
        
        # Input file selection
        input_frame = ttk.Frame(file_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_frame, text="WorkWave CSV File:").pack(side=tk.LEFT, padx=5)
        self.input_path_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.input_path_var, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(input_frame, text="Browse...", command=self.browse_input_file).pack(side=tk.LEFT, padx=5)
        
        # Output file selection
        output_frame = ttk.Frame(file_frame)
        output_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(output_frame, text="Output CSV File:").pack(side=tk.LEFT, padx=5)
        self.output_path_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.output_path_var, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(output_frame, text="Browse...", command=self.browse_output_file).pack(side=tk.LEFT, padx=5)
        
        # Settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="10")
        settings_frame.pack(fill=tk.X, pady=10)
        
        # Pickup location settings
        pickup_frame = ttk.Frame(settings_frame)
        pickup_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(pickup_frame, text="Pickup Location ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.pickup_id_var = tk.StringVar(value=self.converter.pickup_location_id)
        ttk.Entry(pickup_frame, textvariable=self.pickup_id_var, width=20).grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(pickup_frame, text="Pickup Location Name:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.pickup_name_var = tk.StringVar(value=self.converter.pickup_location_name)
        ttk.Entry(pickup_frame, textvariable=self.pickup_name_var, width=20).grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(pickup_frame, text="Pickup Phone Number:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.pickup_phone_var = tk.StringVar(value=self.converter.pickup_phone_number)
        ttk.Entry(pickup_frame, textvariable=self.pickup_phone_var, width=20).grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(pickup_frame, text="Timezone:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.timezone_var = tk.StringVar(value=self.converter.timezone)
        ttk.Entry(pickup_frame, textvariable=self.timezone_var, width=20).grid(row=0, column=3, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(pickup_frame, text="Pickup Window Start:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        self.pickup_start_var = tk.StringVar(value=self.converter.pickup_window_start)
        ttk.Entry(pickup_frame, textvariable=self.pickup_start_var, width=20).grid(row=1, column=3, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(pickup_frame, text="Pickup Window End:").grid(row=2, column=2, sticky=tk.W, padx=5, pady=2)
        self.pickup_end_var = tk.StringVar(value=self.converter.pickup_window_end)
        ttk.Entry(pickup_frame, textvariable=self.pickup_end_var, width=20).grid(row=2, column=3, sticky=tk.W, padx=5, pady=2)
        
        # Pickup instructions
        instructions_frame = ttk.Frame(settings_frame)
        instructions_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(instructions_frame, text="Pickup Instructions:").pack(side=tk.LEFT, padx=5, pady=2)
        self.pickup_instructions_var = tk.StringVar(value=self.converter.pickup_instructions)
        ttk.Entry(instructions_frame, textvariable=self.pickup_instructions_var, width=60).pack(side=tk.LEFT, padx=5, pady=2, fill=tk.X, expand=True)
        
        # Default dropoff instructions
        dropoff_frame = ttk.Frame(settings_frame)
        dropoff_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(dropoff_frame, text="Default Dropoff Instructions:").pack(side=tk.LEFT, padx=5, pady=2)
        self.default_dropoff_var = tk.StringVar(value=self.converter.default_dropoff_instructions)
        ttk.Entry(dropoff_frame, textvariable=self.default_dropoff_var, width=60).pack(side=tk.LEFT, padx=5, pady=2, fill=tk.X, expand=True)
        
        # Conversion button
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        self.convert_button = ttk.Button(button_frame, text="Convert", command=self.convert)
        self.convert_button.pack(side=tk.LEFT, padx=5)
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Status text
        self.status_text = tk.Text(status_frame, height=10, width=80, wrap=tk.WORD)
        self.status_text.pack(fill=tk.BOTH, expand=True)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self.status_text, command=self.status_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.status_text.config(yscrollcommand=scrollbar.set)
        
        # Set initial status
        self.log("Ready to convert WorkWave CSV to DoorDash CSV.")
        
    def browse_input_file(self):
        """Open file dialog to select input file."""
        file_path = filedialog.askopenfilename(
            title="Select WorkWave CSV File",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if file_path:
            self.input_path_var.set(file_path)
            # Auto-generate output file path
            output_path = os.path.splitext(file_path)[0] + "_doordash.csv"
            self.output_path_var.set(output_path)
            self.log(f"Selected input file: {file_path}")
    
    def browse_output_file(self):
        """Open file dialog to select output file."""
        file_path = filedialog.asksaveasfilename(
            title="Save DoorDash CSV File",
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if file_path:
            self.output_path_var.set(file_path)
            self.log(f"Selected output file: {file_path}")
    
    def log(self, message):
        """Add message to status text."""
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
    
    def update_converter_settings(self):
        """Update converter settings from GUI values."""
        self.converter.pickup_location_id = self.pickup_id_var.get()
        self.converter.pickup_location_name = self.pickup_name_var.get()
        self.converter.pickup_phone_number = self.pickup_phone_var.get()
        self.converter.pickup_instructions = self.pickup_instructions_var.get()
        self.converter.pickup_window_start = self.pickup_start_var.get()
        self.converter.pickup_window_end = self.pickup_end_var.get()
        self.converter.timezone = self.timezone_var.get()
        self.converter.default_dropoff_instructions = self.default_dropoff_var.get()
    
    def convert(self):
        """Convert WorkWave CSV to DoorDash CSV."""
        input_file = self.input_path_var.get()
        output_file = self.output_path_var.get()
        
        if not input_file:
            messagebox.showerror("Error", "Please select an input file.")
            return
        
        if not output_file:
            messagebox.showerror("Error", "Please select an output file.")
            return
        
        try:
            self.log("Starting conversion...")
            self.convert_button.config(state=tk.DISABLED)
            self.root.update()
            
            # Update converter settings
            self.update_converter_settings()
            
            # Perform conversion
            count = self.converter.convert_file(input_file, output_file)
            
            self.log(f"Conversion complete! {count} orders processed.")
            self.log(f"Output saved to: {output_file}")
            
            messagebox.showinfo("Success", f"Conversion complete! {count} orders processed.")
        except Exception as e:
            self.log(f"Error: {str(e)}")
            messagebox.showerror("Error", str(e))
        finally:
            self.convert_button.config(state=tk.NORMAL)


def main():
    """Main function to run the application."""
    root = tk.Tk()
    app = ConverterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()