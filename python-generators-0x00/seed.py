import mysql.connector
import csv
import uuid

# --- Database Configuration ---
DB_HOST = "localhost"
DB_USER = "alx_user"
DB_PASSWORD = "user_password"
DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"
CSV_FILE = "user_data.csv"

# --- Connect to the MYSQL database server
def connect_db():
    """
    Connects to the MySQL database server.
    Returns the connection object.
    """
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        if connection.is_connected():
            print(f"Successfully connected to MySQL Server (Host: {DB_HOST}, User: {DB_USER})")
            return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL Server: {e}")
        return None

 # --- Create the database ALX_prodev if it does not exist ---
def create_database(connection):
    """
    Creates the ALX_prodev database if it does not exits.
    Requires a connection to the MySQl server.
    """
    if not connection:
        print("No database connection provided to create database.")
        return False
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database '{DB_NAME}' ensured to exist.")
        cursor.close()
        return True
    except mysql.connector.Error as e:
        print(f"Error creating database '{DB_NAME}': {e}")
        return False

# --- Connect to the ALX_prodev database ---
def connect_to_prodev():
    """
    Connects to the ALX_prodev database in MySQL.
    Returns the connection object.
    """
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if connection.is_connected():
            print(f"Successfully connected to database '{DB_NAME}'")
            return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to database '{DB_NAME}': {e}")
        return None

# --- Create the user_data table if it does not exists ---
def create_table(connection):
    """
    Creates the 'user_data' table if it deos not exist with the required fields.
    Requires a connection to the ALX_prodev database.
    """
    if not connection:
        print("No database connection provided to create table")
        return False
    try:
        cursor = connection.cursor()
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            user_id VARCHAR(40) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            age DECIMAL(5, 2) NOT NULL
        );
        """
        cursor.execute(create_table_query)
        # cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_{TABLE_NAME}_user_id ON {TABLE_NAME} (user_id);")
        print(f"Table '{TABLE_NAME}' ensured to exist.")
        connection.commit() # Commit DDL operations
        cursor.close()
        return True
    except mysql.connector.Error as e:
        print(f"Error creating table '{TABLE_NAME}': {e}")
        return False


# --- Inserting data to the database (if it does not exists) ---
def insert_data(connection, csv_filepath):
    """
    Inserts data into the 'user_data' table.
    Generates a new UUID for each user_id if not provided in data.
    Uses INSERT IGNORE to prevent errors on duplicate entries(based on Primary key).
    Requires a connctionn to connect to the ALX_prodev database.

    Args:
        connection: An active MySQL database connection object.
        csv_filepath (str): The path to the CSV file containing user data.
    """
    if not connection:
        print("No database connection provided to insert data.")
        return False
    
    user_data = []
    try:
        # open the csv file and read its content
        with open(csv_filepath, mode='r', newline='', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                user_data.append(row)
            
            if not user_data: # Check for empty user data after trying to read from it
                print(f"No data found in '{csv_filepath}' to insert.")
                return False
            
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_filepath}' not found. Please ensure the path is correct.")
        return False
    except Exception as e: # Catch other potential file reading errors.
        print(f"An error occured while reading CSV file '{csv_filepath}': {e}")
        return False

    try:
        cursor = connection.cursor()
        # INSERT IGNORE allows the re-run of the script without errors
        # if the same data (same user_id if already present) is attempted to be inserted.
        insert_query = f"""
        INSERT IGNORE INTO {TABLE_NAME}
            (user_id, name, email, age)
        VALUES(%s, %s, %s, %s)
        """

        # Data with generated UUIDs.
        rows_to_insert = []
        for row_dict in user_data:
            new_user_id = str(uuid.uuid4())
            rows_to_insert.append((new_user_id, row_dict['name'], row_dict['email'], float(row_dict['age'])))

        cursor.executemany(insert_query, rows_to_insert)
        connection.commit()
        print(f"Successfully inserted {cursor.rowcount} rows into '{TABLE_NAME}'.")
        cursor.close()
        return True
    except mysql.connector.Error as e:
        print(f"Error inserting data into '{TABLE_NAME}': {e}")
        return False