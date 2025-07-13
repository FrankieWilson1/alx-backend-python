from decimal import Decimal
import mysql.connector

# --- Database Configuration ---
DB_HOST = "localhost"
DB_USER = "alx_user"
DB_PASSWORD = "user_password"
DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"

def stream_users_in_batches(batch_size):
    """
    Generator function to fetch rows from the 'user_data' table in batches.
    Yields a list of rows (each row as a dictionary).
    This function contains exactly 1 loop for fetching batches.
    """
    if not isinstance(batch_size, int) or batch_size <= 0:
        raise ValueError("batch_size must be a positive integer.")
    
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if not connection.is_connected():
            print(f"Error: Could not connect to database '{DB_NAME}'.")
            return
        
        cursor = connection.cursor(dictionary=True, buffered=True)
        select_query = f"SELECT user_id, name, email, age FROM {TABLE_NAME}"
        cursor.execute(select_query)
        
        while True: # Loop (total): Fetches batches of data
            batch = cursor.fetchmany(batch_size)
            if not batch:   # No more rows.
                break
            yield batch
    except mysql.connector.Error as e:
        print(f"Database error during batch streaming: {e}")
    except Exception as e:
        print(f"An unexpected error occured in stream_users_in_batches: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def batch_processing(batch_size):
    """
    Generator function that processes batches of users from 'stream_uusers_in_batches'.
    Filters users over the age of 25 and converts 'age' from Decimal to int.
    Yields a list of filtered users for each batch.
    This function contains 2 loops(one for batchs, one for users within a batch).
    """
    for batch in stream_users_in_batches(batch_size):
        filtered_batch = []
        for user in batch:
            current_age = user.get('age')
            if isinstance(current_age, Decimal):
                current_age = int(current_age)
                user['age'] = current_age # Update the dictionary with the int age
            
            if current_age is not None and current_age > 25:
                filtered_batch.append(user)
                try:
                    print(user)
                except OSError as e:
                    # This takes care of errno 22 (Invalid argument) or 32 (Broken pipe) on windows or Linux respectivel
                    if e.errno == 22 or e.errno == 32:
                        return # Exit batch_processing function gracefully
                    else:
                        raise   # Other OSError.
                    