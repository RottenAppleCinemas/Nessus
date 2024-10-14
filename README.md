This project automates the export, transformation, and uploading of Nessus vulnerability scan data into a PostgreSQL database. It consists of three Python scripts:

1. **extract_scan.py**: Exports Nessus scans in `.nessus` format.
2. **csv_transform.py**: Transforms the exported `.nessus` files into CSV format.
3. **UPLOAD.PY**: Uploads the CSV files to a PostgreSQL database.

---

## Requirements

- Python 3.x
- Libraries:
  - `requests`
  - `xml.etree.ElementTree`
  - `pandas`
  - `sqlalchemy`
  - `argparse`
  - `tqdm`
  - `subprocess`
  - `os`
  - `logging`

You can install the necessary libraries using `pip`:

```bash
pip install requests pandas sqlalchemy tqdm
```

---

## Script 1: `extract_scan.py`

This script handles the process of logging into Nessus, exporting scan files, and saving them locally. 
**"py extract_scan.py user password https://127.0.0.1:8834 --output "C:\Users\Administrator\Documents\Nessus"**

### Features:

- Connects to Nessus using a username, password, and the URL of the Nessus server.
- Retrieves folders and scans, then exports each scan in `.nessus` format.
- Saves the exported files to the specified output directory.
- Uses logging to track both successful and error events.

### Usage:

```bash
python extract_scan.py <username> <password> <url> --output <output_folder>
**"py extract_scan.py Michael Walnut2023!! https://127.0.0.1:8834 --output "C:\Users\Administrator\Documents\Nessus"**
```

- **username**: Nessus account username.
- **password**: Nessus account password.
- **url**: Nessus server URL.
- **output** (optional): The directory where the exported scans will be saved (default is `export`).

After all scans are exported, it triggers the **csv_transform.py** script automatically.

### Example:

```bash
python extract_scan.py admin mypassword https://nessus-server --output ./nessus_exports
```

---

## Script 2: `csv_transform.py`

This script transforms Nessus `.nessus` XML files into CSV format for easier analysis and processing. It processes files from multiple directories and saves the CSV output into a specified folder.

### Features:

- Parses `.nessus` files to extract vulnerability information.
- Converts the extracted data into a Pandas DataFrame.
- Exports the DataFrame to a CSV file for each folder.
- Automatically triggers **UPLOAD.PY** to upload the CSV data to a PostgreSQL database.

### Usage:

This script is automatically triggered by `extract_scan.py`. No manual invocation is required unless running it independently.

---

## Script 3: `UPLOAD.PY`

This script uploads the transformed CSV files to a PostgreSQL database.

### Features:

- Maps CSV files to specific PostgreSQL tables.
- Loads the CSV content into the appropriate table.
- Replaces existing data in the tables if they already exist.

### Configuration:

Before running the script, you need to configure your database connection by filling in the appropriate values in the script:
- **db_name**: The name of your PostgreSQL database.
- **user**: Your PostgreSQL username.
- **password**: Your PostgreSQL password.
- **host**: The host of the PostgreSQL database (default: `localhost`).
- **port**: The port of the PostgreSQL database (default: `5432`).

### Usage:

This script is automatically triggered by `csv_transform.py` after CSV generation. No manual invocation is required unless running it independently.

---

## Logging

- **Error logs**: Located in the `logs/error.log` file.
- **Success logs**: Located in the `logs/success.log` file.
Both log files will be created in the output directory specified.

---

## Notes

- Ensure that the Nessus server credentials and the URL are correctly specified in **extract_scan.py**.
- Make sure that PostgreSQL is installed and the database is set up before running the **UPLOAD.PY** script.

This set of scripts can automate the end-to-end process from scan export to database upload, making vulnerability management much more efficient.
