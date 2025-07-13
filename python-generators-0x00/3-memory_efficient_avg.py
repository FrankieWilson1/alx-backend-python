from decimal import Decimal
import mysql.connector
import sys

# --- Database Configuration ---
DB_HOST = "localhost"
DB_USER = "alx_user"
DB_PASSWORD = "user_password"
DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"

def stream_user_ages():
    """
    Generator function that yields user ages one by one directly from the database.
    This ensures memory efficiencey as the entire age list not loaded at once.
    """
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
            print(f"Error: Could not connect to database '{DB_NAME}'. Please check connection detials .", file=sys.stderr)
            return   # Generator simply stops if it cannot proceed.
        
        cursor = connection.cursor(dictionary=True, buffered=True)
        
        # Select only the 'age' column to minimize data fetched per row
        select_query = f"SELECT age FROM {TABLE_NAME}"
        cursor.execute(select_query)
        
        #   Loops iterates directly over the cursor results.
        for row in cursor:
            age = row.get('age')
            if age is not None:
                if isinstance(age, Decimal):
                    age = int(age)
                yield age
    except mysql.connector.Error as e:
        print(f"Database error in stream_user_ages: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occured in stream_user_ages: {e} ", file=sys.stderr)
    finally:
        # closes database resources.
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def calculate_average_age():
    """
    Calculates the average age of users by consuming ages one by one
    from the stream_user_age generator function, ensuring memory efficiencey.
    Returns the calculated average age.
    
    """
    total_age = 0
    count_users = 0
    
    for age in stream_user_ages():
        total_age += age
        count_users += 1
        
    if count_users == 0:
        return 0.0  # Returns 0.0 as the average age.
    
    return total_age