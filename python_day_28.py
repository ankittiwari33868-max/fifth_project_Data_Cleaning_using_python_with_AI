# Day 28 of python challenge
# solve real world problems with python

import os
import pandas as pd

# Ask user for folder path
folder_path = input("Enter the folder path containing CSV files: ").strip()

# Check if folder exists
if not os.path.exists(folder_path):
    print("Invalid folder path!")
    exit()

# Get all CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

if not csv_files:
    print("No CSV files found in the folder!")
    exit()

# Output Excel file path
output_file = os.path.join(folder_path, "ALL_CSV_Converted_into_Sheets.xlsx")

# Create Excel writer
with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        
        # Read CSV
        df = pd.read_csv(file_path)
        
        # Sheet name = file name without extension (max 31 chars for Excel)
        sheet_name = os.path.splitext(file)[0][:31]
        
        # Write to Excel sheet
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"\nAll CSV files have been combined into:\n{output_file}")