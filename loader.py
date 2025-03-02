import concurrent.futures
import pandas as pd
import psycopg2
import requests
from dotenv import load_dotenv
import os
# load DATABASE_URL from environment variable
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

#  CSV Files to Read
CSV_FILES = ["Salary_Data.csv","cafe_sales.csv"]

#  API Endpoint
API_URL = "https://jsonplaceholder.typicode.com/users"

#  Function to load data from CSV
def load_csv(file_path):
    print(f"[CSV] Loading {file_path}...")
    df = pd.read_csv(file_path)
    print(f"[CSV] Loaded {len(df)} rows from {file_path}")
    return df

#  Function to fetch data from API
def fetch_api():
    print("[API] Fetching data...")
    response = requests.get(API_URL)
    data = response.json()
    print(f"[API] Received {len(data)} records")
    return data

#  Function to fetch data from PostgreSQL
def fetch_database():
    print("[DB] Querying PostgreSQL database...")
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")  # Modify based on your table structure
    data = cursor.fetchall()
    conn.close()
    print(f"[DB] Retrieved {len(data)} records")
    return data

#  Using ThreadPoolExecutor for Concurrent Execution
executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)

# Submitting CSV tasks individually
future_csv_list = []
for file in CSV_FILES:
    future = executor.submit(load_csv, file)
    future_csv_list.append(future)

#  Submitting API task
future_api = executor.submit(fetch_api)

#  Submitting Database task
future_db = executor.submit(fetch_database)

#  Retrieving results explicitly
csv_data_list = []
for future in future_csv_list:
    result = future.result()
    csv_data_list.append(result)

api_data = future_api.result()
db_data = future_db.result()

#  Shutdown the ThreadPoolExecutor
executor.shutdown()

#  Combine all data into a dictionary
all_data = {
    "csv_data": csv_data_list,
    "api_data": api_data,
    "db_data": db_data
}
# print data got from csv files

print("All data from CSV files:")
for data in all_data["csv_data"]:
    print(data.head())
# print data got from API
print("All data from API:")
print(all_data["api_data"])

# print data got from database
print("All data from database:")
print(all_data["db_data"])

print("All data loaded successfully!")
