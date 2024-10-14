import pandas as pd
from sqlalchemy import create_engine

# Configuration.
csv_table_mapping = {
    "C:/Users/Administrator/Documents/Nessus/reportpg/example.csv": "Table name here",
    "C:/Users/Administrator/Documents/Nessus/reportpg/example.csv": "Table name here",
    "C:/Users/Administrator/Documents/Nessus/reportpg/example.csv": "Table name here",
    "C:/Users/Administrator/Documents/Nessus/reportpg/example.csv": "Table name here",
    "C:/Users/Administrator/Documents/Nessus/reportpg/example.csv": "Table name here"
}

db_name = "database name here"  # Database name
user = "user"  # Your PostgreSQL username
password = "password"  # Your PostgreSQL password
host = "localhost"  # Host address
port = "5432"  # Default PostgreSQL port

# Create a connection to PostgreSQL
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')

# Loop through the dictionary and process each CSV file
for csv_file_path, table_name in csv_table_mapping.items():
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(csv_file_path)

        # Write the DataFrame to the PostgreSQL table
        df.to_sql(table_name, engine, if_exists='replace', index=False)

        print(f"Data from {csv_file_path} has been successfully imported into the {table_name} table in the {db_name} database.")
    
    except Exception as e:
        print(f"An error occurred while processing {csv_file_path}: {e}")
