import argparse
import requests
import os
import urllib3
import logging
from tqdm import tqdm
import subprocess  # Import subprocess module

# Suppress only the single InsecureRequestWarning from urllib3 needed for self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Function to configure logging
def setup_logging(output_folder):
    log_dir = os.path.join(output_folder, "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    # Set up logging for errors
    error_log_file = os.path.join(log_dir, "error.log")
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s', filename=error_log_file, filemode='w')
    
    # Set up a separate logger for successes
    success_logger = logging.getLogger("success_logger")
    
    # Ensure success logger doesn't propagate to root logger
    success_logger.propagate = False
    
    success_handler = logging.FileHandler(os.path.join(log_dir, "success.log"))
    success_handler.setLevel(logging.INFO)
    success_formatter = logging.Formatter('%(asctime)s - %(message)s')
    success_handler.setFormatter(success_formatter)
    
    # Add the handler only for the success logger
    success_logger.addHandler(success_handler)
    success_logger.setLevel(logging.INFO)
    
    return success_logger

def login(username, password, url):
    print("Logging in...")
    login_url = f"{url}/session"
    payload = {'username': username, 'password': password}
    response = requests.post(login_url, json=payload, verify=False)
    response.raise_for_status()
    print("Login successful.")
    return response.json()['token']

def get_folders(token, url):
    print("Retrieving folders...")
    headers = {'X-Cookie': f'token={token}'}
    folders_url = f"{url}/folders"
    response = requests.get(folders_url, headers=headers, verify=False)
    response.raise_for_status()
    print("Folders retrieved.")
    return response.json()['folders']

def get_scans(token, url):
    print("Retrieving scans...")
    headers = {'X-Cookie': f'token={token}'}
    scans_url = f"{url}/scans"
    response = requests.get(scans_url, headers=headers, verify=False)
    response.raise_for_status()
    print("Scans retrieved.")
    return response.json()['scans']

def export_scan(token, url, scan_id, scan_name, output_folder, success_logger):
    print(f"Exporting scan '{scan_name}'...")
    headers = {'X-Cookie': f'token={token}'}
    export_url = f"{url}/scans/{scan_id}/export"
    payload = {'format': 'nessus'}

    try:
        response = requests.post(export_url, headers=headers, json=payload, verify=False)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            logging.error(f"Scan '{scan_name}' not found (404).")
            return None  # Skip if scan is not found (404)
        elif response.status_code == 409:
            logging.error(f"Scan '{scan_name}' is currently being exported or there is a conflict (409).")
            return None  # Skip if there's a conflict (409)
        else:
            logging.error(f"Error: {err}")
            raise  # Re-raise for other errors

    file_id = response.json()['file']
    
    # Polling the export status
    while True:
        status_url = f"{url}/scans/{scan_id}/export/{file_id}/status"
        try:
            response = requests.get(status_url, headers=headers, verify=False)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            if response.status_code == 500:
                logging.error(f"Server encountered an internal error (500) while exporting scan '{scan_name}'.")
                return None  # Skip this scan if there's a 500 error
            else:
                logging.error(f"Error: {err}")
                raise  # Re-raise for other errors

        if response.json()['status'] == 'ready':
            break

    download_url = f"{url}/scans/{scan_id}/export/{file_id}/download"
    try:
        response = requests.get(download_url, headers=headers, stream=True, verify=False)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            logging.error(f"File for scan '{scan_name}' not found (404). Skipping download.")
            return None  # Skip if file is not found (404)
        else:
            logging.error(f"Error: {err}")
            raise  # Re-raise for other errors

    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    t = tqdm(total=total_size, unit='iB', unit_scale=True, unit_divisor=1024, desc=f"Downloading {scan_name}", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [speed: {rate_fmt}]")
    content = b""
    for data in response.iter_content(block_size):
        t.update(len(data))
        content += data
    t.close()
    
    # Log success
    success_logger.info(f"Scan '{scan_name}' exported successfully.")
    print(f"Scan '{scan_name}' exported.")
    return content

def save_scan_to_file(content, filepath):
    print(f"Saving scan to '{filepath}'...")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'wb') as f:
        f.write(content)
    print(f"Scan saved to '{filepath}'.")

def main(username, password, url, output_folder):
    success_logger = setup_logging(output_folder)  # Initialize logging

    try:
        token = login(username, password, url)
        folders = get_folders(token, url)
        scans = get_scans(token, url)
        
        folder_map = {folder['id']: folder['name'] for folder in folders}
        
        for scan in scans:
            folder_name = folder_map.get(scan['folder_id'], 'Default Folder')
            scan_name = scan['name']
            scan_id = scan['id']
            
            file_content = export_scan(token, url, scan_id, scan_name, output_folder, success_logger)
            if file_content:
                filepath = os.path.join(output_folder, folder_name, f"{scan_name}.nessus")
                save_scan_to_file(file_content, filepath)
                
        # Trigger csv_transform.py after all scans are processed
        subprocess.run(['python', r'C:\Users\Administrator\Documents\Py scripts\Nessus\csv_transform.py'], check=True)
    
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting...")
        exit()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print("An error occurred. Check the logs for more details.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Export Nessus scans to .nessus files')
    parser.add_argument('username', help='Nessus username')
    parser.add_argument('password', help='Nessus password')
    parser.add_argument('url', help='Nessus URL')
    parser.add_argument('--output', default='export', help='Output folder for the exported scans')
    
    args = parser.parse_args()
    main(args.username, args.password, args.url, args.output)
