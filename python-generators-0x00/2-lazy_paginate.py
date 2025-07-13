from decimal import Decimal
import mysql.connector
import sys

# --- Database Configuration ---
DB_HOST = "localhost"
DB_USER = "alx_user"
DB_PASSWORD = "user_password"
DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"

def paginate_users(page_size, offset):
    """
    Fetches a single page of users from the database.
    Returns a list of user dictionaries for the given page size and offset.
    Returns an empty list if no moare users are found.
    """
    connection = None
    cursor = None
    users_on_page = []
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if not connection.is_connected():
            print(f"Error: Could not connect to database '{DB_NAME}'. Please check connection detials .", file=sys.stderr)
            return []   # Returns an empty lists.
        
        cursor = connection.cursor(dictionary=True, buffered=True)
        
        # Placeholders are used to safely pass page_size and offset args.
        select_query = f"SELECT user_id, name, email, age FROM {TABLE_NAME} LIMIT %s OFFSET %s"
        cursor.execute(select_query, (page_size, offset))
        
        # All the results for this specific page.
        users_on_page = cursor.fetchall()
        
        # Decimal convertion for 'age' to int for each user in the fetched page.
        for user in users_on_page:
            if 'age' in user and isinstance(user['age'], Decimal):
                user['age'] = int(user['age'])
        
        return users_on_page
    
    except mysql.connector.Error as e:
        print(f"Database error during page fetching: {e}", file=sys.stderr)
        return []   # empty list on DB error
    except Exception as e:
        print(f"An unexpected error occured in paginate_users: {e}", file=sys.stderr)
        return []   # General error.
    finally:
        if cursor:
            cursor.close()  # Ensures cursor closure
        if connection and connection.is_connected():
            connection.close();
            
def lazy_pagination(page_size):
    """
    Generator function that lazily loads pages of users from the database.
    It fetches the next page only when requested, using paginate_users function internally.
    This function uses only one loop
    Yields a list of user dictinaries for each page.
    """
    if not isinstance(page_size, int) or page_size <= 0:
        raise ValueError("page_size must be a positive integer.")
    
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        
        if not page:
            break   # Exit generator loop if page is empty
        
        yield page  # yield the entire page
        offset += page_size