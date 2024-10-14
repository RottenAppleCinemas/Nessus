import xml.etree.ElementTree as ET
import pandas as pd
import os
import subprocess

# Define the list of directories containing the .nessus files
directories = [
    r'C:\Users\Administrator\Documents\Nessus\folder1',
    r'C:\Users\Administrator\Documents\Nessus\folder2',
    r'C:\Users\Administrator\Documents\Nessus\folder3',
    r'C:\Users\Administrator\Documents\Nessus\folder4',
    r'C:\Users\Administrator\Documents\Nessus\folder5'
]

# Directory where CSVs will be saved
output_directory = r'C:\Users\Administrator\Documents\Py scripts\Nessus\reportpg'

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Iterate over each directory
for directory_path in directories:
    # Prepare a list to hold all report data for the current directory
    all_data = []

    # Iterate over each .nessus file in the specified directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.nessus'):
            file_path = os.path.join(directory_path, filename)  # Full path to the file
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Get the base file name without the .nessus extension
            base_file_name = os.path.splitext(filename)[0]
            
            # Iterate over each ReportItem in the XML
            for report_item in root.findall('.//ReportItem'):
                item_data = {'file_name': base_file_name}  # Add the base file name to each record
                
                # Capture all child elements
                for child in report_item:
                    item_data[child.tag] = child.text.strip() if child.text else ''
                
                # Capture all attributes
                for attr in report_item.attrib:
                    item_data[attr] = report_item.attrib[attr]
                
                all_data.append(item_data)

    # Create a DataFrame for the current directory's data
    df = pd.DataFrame(all_data)

    # Define the CSV file name based on the folder name
    folder_name = os.path.basename(directory_path)
    csv_file_path = os.path.join(output_directory, f'{folder_name}.csv')

    # Save the DataFrame to a CSV file
    df.to_csv(csv_file_path, index=False)

    print(f"Data from {directory_path} has been successfully written to {csv_file_path}")

# Trigger the UPLOAD.PY script after CSV generation is complete. The Upload script will send the data to postgres.
upload_script_path = r'C:\Users\Administrator\Documents\Nessus\UPLOAD.PY'
subprocess.run(['python', upload_script_path], check=True)

print(f"{upload_script_path} has been successfully triggered.")
