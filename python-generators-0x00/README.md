# Python Generators 0x00 - Memory-Efficient Data Processing

This repository contains solutions to tasks focusing on implementing and utilizing Python generators for memory-efficient data processing, particularly when interacting with large datasets from a MySQL database. The project demonstrates how generators can be used for streaming, batch processing, lazy pagination, and aggregate calculations without loading entire datasets into memory.

## Table of Contents

- [Python Generators 0x00 - Memory-Efficient Data Processing](#python-generators-0x00---memory-efficient-data-processing)
  - [Table of Contents](#table-of-contents)
  - [Project Description](#project-description)
  - [Project Structure](#project-structure)
  - [Setup and Installation](#setup-and-installation)
  - [Database Setup](#database-setup)
    - [Configure Database Credentials](#configure-database-credentials)
    - [Run the Seeder Script](#run-the-seeder-script)
  - [Usage](#usage)
    - [Task 0: User Streaming](#task-0-user-streaming)
    - [Task 1: Batch Processing](#task-1-batch-processing)
    - [Task 2: Lazy Pagination](#task-2-lazy-pagination)
    - [Task 3: Memory-Efficient Average](#task-3-memory-efficient-average)
  - [Key Concepts Demonstrated](#key-concepts-demonstrated)
  - [Author](#author)

## Project Description

This project explores the power of Python generators for handling large volumes of data efficiently. By yielding data points or batches only when requested, generators prevent excessive memory consumption, making them ideal for backend operations involving databases. The tasks cover various real-world scenarios such as:

- Streaming individual records.
- Processing data in manageable batches.
- Implementing lazy, paginated data retrieval.
- Performing aggregate calculations (like average) without in-memory storage of all data.

All tasks interact with a MySQL database.

## Project Structure

```
.
├── 0-stream_users.py
├── 1-batch_processing.py
├── 2-main.py             # Driver script for 1-batch_processing.py
├── 2-lazy_paginate.py
├── 3-main.py             # Driver script for 2-lazy_paginate.py
├── 4-main.py             # Driver script for 3-memory_efficient_avg.py
├── 3-memory_efficient_avg.py # (Assuming this is the final name for the avg task)
├── seed.py
└── user_data.csv         # CSV file containing mock user data for seeding the database
```

- **`seed.py`**: Responsible for setting up the MySQL database (`ALX_prodev`) and table (`user_data`) schema, and populating it with mock user data (user_id, name, email, age). This is crucial for running all other scripts.
- **`user_data.csv`**: A comma-separated values file containing mock user data that is used by `seed.py` to populate the database. Ensure this file is in the same directory as the scripts.
- **`0-stream_users.py`**: Contains the `stream_users()` generator function which connects to the database and yields user records one by one, demonstrating basic memory-efficient data streaming.
- **`1-batch_processing.py`**: Implements `stream_users_in_batches(batch_size)` generator to fetch data in predefined batches. It also includes `batch_processing(batch_size)` which consumes these batches, filters users (age > 25), and prints them directly, handling `OSError` (e.g., Broken Pipe) gracefully within the function.
- **`2-main.py`**: A driver script designed to run `1-batch_processing.py`'s `batch_processing` function. It includes `OSError` handling for cases where output is piped (e.g., `| head -n 5`), ensuring graceful exit.
- **`2-lazy_paginate.py`**: Provides `paginate_users(page_size, offset)` for fetching specific pages from the database. It then defines `lazy_paginate(page_size)`, a generator that lazily yields pages of users, fetching them only when requested by the consumer.
- **`3-main.py`**: A driver script for `2-lazy_paginate.py`. It iterates through the pages yielded by `lazy_paginate` and prints individual users, incorporating `OSError` handling for piped output scenarios.
- **`3-memory_efficient_avg.py`**: Features `stream_user_ages()` generator that yields user ages one by one. It also contains `calculate_average_age()` which consumes these ages to compute the average without loading all data into memory, adhering to a two-loop limit for the entire calculation process.

## Setup and Installation

To run these scripts, you will need:

1. **Python 3.x**: Ensure Python 3 is installed on your system.
2. **MySQL Server**: A running MySQL server instance.
3. **`mysql-connector-python`**: The official MySQL driver for Python.

You can install the required Python library using pip:

```bash
pip install mysql-connector-python
```

## Database Setup

Before running any script, you must set up your database and populate it using `seed.py`.

### Configure Database Credentials

Open `seed.py` (and all other .py files that connect to the database) and ensure the following constants match your MySQL setup:

```python
# --- Database Configuration ---
DB_HOST = "localhost"
DB_USER = "alx_user"
DB_PASSWORD = "user_password"
DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"
```

It's highly recommended to use a strong password for your MySQL user.

### Run the Seeder Script

Execute `seed.py` once to create the database and table, and populate it with mock data.

```bash
python3 seed.py
```

You should see output indicating successful database and table creation, and data insertion.

## Usage

Each task is demonstrated by running its respective Python script.

### Task 0: User Streaming

Streams all users one by one from the database.

```bash
python3 0-stream_users.py
```

### Task 1: Batch Processing

Streams users in batches, filters them (age > 25), and prints. This task often uses piping for demonstration, which is why `2-main.py` handles `OSError`.

```bash
# Run the batch processing and see all output
python3 2-main.py

# Run with a pipe to 'head' to demonstrate memory efficiency and OSError handling
# (e.g., to see only the first 5 processed users)
python3 2-main.py | head -n 5
```

### Task 2: Lazy Pagination

Demonstrates fetching users page by page lazily. The `3-main.py` script consumes the pages and prints users.

```bash
# Run the lazy pagination and see all output
python3 3-main.py

# Run with a pipe to 'head' to demonstrate memory efficiency and OSError handling
# (e.g., to see only the first 10 processed users)
python3 3-main.py | head -n 10
```

### Task 3: Memory-Efficient Average

Calculates the average age of users without loading all ages into memory.

```bash
python3 3-memory_efficient_avg.py
```

## Key Concepts Demonstrated

- **Generators (yield)**: Creating iterable sequences that produce values on demand, saving memory.
- **Memory Efficiency**: Processing large datasets without storing them entirely in RAM.
- **Database Interaction**: Connecting to and querying a MySQL database using `mysql-connector-python`.
- **Batch Processing**: Handling data in chunks for efficient processing.
- **Lazy Pagination**: Retrieving data in pages only when the next page is needed.
- **Aggregate Functions (Manual)**: Performing calculations like average iteratively.
- **Error Handling (OSError, BrokenPipeError)**: Gracefully managing errors that occur when output streams are closed (e.g., when piping to head).

## Author

Frank Williams Ugwu

