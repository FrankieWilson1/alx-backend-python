from decimal import Decimal
import mysql.connector

# --- Database Configuration ---
DB_HOST = "localhost"
DB_USER = "alx_user"
DB_PASSWORD = "user_password"
DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"

def stream_users():
    """Generator function to fetch rows one by one from the 'user_table' table.
       It connects to the ALX_prodev database and yields each row as a tuple.
       Has no more than 1 loop.
    """
    connection = None
    cursor = None
    try:
        # Establish a connection to the ALX_prodev database
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        
        if not connection.is_connected():
            print(f"Error: Could not connect to database '{DB_NAME}'. Please check connection details.")
            return  # If the connection fails.
        
        cursor = connection.cursor(dictionary=True, buffered=True)
        
        select_query = f"SELECT user_id, name, email, age FROM {TABLE_NAME}"
        cursor.execute(select_query)
        
        # Iterate through the fetched rows and yield each one(singel loop allowed)
        for row in cursor:
            if 'age' in row and isinstance(row['age'], Decimal):
                row['age'] = int(row['age'])
            yield row
            
    except mysql.connector.Error as e:
        print(f"Database error during streaming: {e}")
    except Exception as e:
        print(f"An unexpected error occured: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()