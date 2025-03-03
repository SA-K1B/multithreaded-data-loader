# Multithreading for Efficient I/O Operations


Modern computing systems perform various types of tasks, which can be broadly categorized into:

**CPU-Bound Tasks**: 
These tasks involve complex calculations that fully engage the CPU. Examples include simulations, image processing, data analysis.

**Example**

A CPU-bound task involves intensive computations that fully utilize the processor.
```python

def cpu_bound_task(n):
    total = 0
    for i in range(n):
        total += i * i  # Heavy computation  # Heavy computation
    return total

cpu_bound_task(10**7)
```

This example performs a CPU-bound task by calculating the sum of squares of numbers up to `n`. The computation is intensive and fully utilizes the CPU.

**I/O-Bound Tasks**: 
These tasks involve waiting for external resources such as disk I/O, network requests, or database queries. Examples include reading files from disk, making API calls, and querying databases.

### Example

An I/O-bound task involves waiting for external resources such as file reading, network requests, or database queries.

```python

import requests

def io_bound_task():
    response = requests.get("https://jsonplaceholder.typicode.com/users")
    return response.json()
    
io_bound_task()
```
This example makes an API request, which requires waiting for the response. Instead of letting the CPU remain idle, multithreading can be used to perform multiple such requests simultaneously.

## How Multithreading Improves I/O-Bound Performance

When a program performs an I/O-bound operation, such as reading a file, making an API request, or querying a database, the CPU must wait until the operation is completed. During this waiting period, the CPU remains idle, which is inefficient. Multithreading enables the program to initiate multiple I/O operations simultaneously, making better use of CPU resources by switching to other tasks while waiting.

### Example: Multithreading in `loader.py`

The script `loader.py` demonstrates how multithreading improves efficiency by loading data from multiple sources concurrently:

1. **Reading data from CSV files** (Disk I/O)
2. **Fetching data from an API** (Network I/O)
3. **Querying a PostgreSQL database** (Database I/O)

#### Function 1: Loading Data from CSV
```python
# Function to load data from CSV

def load_csv(file_path):
    print(f"[CSV] Loading {file_path}...")
    df = pd.read_csv(file_path)
    print(f"[CSV] Loaded {len(df)} rows from {file_path}")
    return df
```
This function reads data from a CSV file, which involves disk I/O. Instead of waiting for each file to be read sequentially, multithreading allows multiple CSV files to be read concurrently.

#### Function 2: Fetching Data from an API
```python
# Function to fetch data from API

def fetch_api():
    print("[API] Fetching data...")
    response = requests.get(API_URL)
    data = response.json()
    print(f"[API] Received {len(data)} records")
    return data
```
This function makes an HTTP request to fetch data from an API. Since network requests have significant latency, using multithreading prevents the CPU from being idle while waiting for the response.

#### Function 3: Fetching Data from PostgreSQL Database
```python
# Function to fetch data from PostgreSQL

def fetch_database():
    print("[DB] Querying PostgreSQL database...")
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users") 
    data = cursor.fetchall()
    conn.close()
    print(f"[DB] Retrieved {len(data)} records")
    return data
```
This function queries a PostgreSQL database. Database queries involve waiting for responses from the database server, making them ideal candidates for multithreading.

## Using `ThreadPoolExecutor` for Multithreading

The script utilizes Python’s `ThreadPoolExecutor` to execute these I/O-bound tasks concurrently:
```python
# Using ThreadPoolExecutor for Concurrent Execution
executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)

# Submitting CSV tasks individually
future_csv_list = []
for file in CSV_FILES:
    future = executor.submit(load_csv, file)
    future_csv_list.append(future)

# Submitting API task
future_api = executor.submit(fetch_api)

# Submitting Database task
future_db = executor.submit(fetch_database)
```
Here, the script assigns:
- Multiple CSV file loading tasks
- API fetching task
- Database querying task

Each task runs in a separate thread, preventing sequential blocking and making efficient use of CPU resources.

### Retrieving Results
After execution, the script collects the results:

```python
csv_data_list = []
for future in future_csv_list:
    result = future.result()
    csv_data_list.append(result)

api_data = future_api.result()
db_data = future_db.result()
```

By retrieving results explicitly, the script ensures that each thread completes before proceeding further.

### Shutting Down the Thread Pool
```python
executor.shutdown()
```
After all tasks are completed, the thread pool is shut down to release system resources.

## Conclusion

Using multithreading with `ThreadPoolExecutor`, the `loader.py` script efficiently handles multiple I/O-bound tasks, significantly improving performance. This approach is particularly useful for applications that need to read large files, make API calls, or interact with databases, as it minimizes idle CPU time and optimizes resource usage.

## Contact

You can connect with me on [![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/tarequl-hasan-sakib/).
