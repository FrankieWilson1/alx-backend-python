import sqlite3 
import functools
import sys


def with_db_connection(func):
    """ 
     decorator that automatically handles opening and closing database connections,
     passes it as the first argument to the decorated function, and ensures the connetion is closed afterward.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            # Open the database connection
            conn = sqlite3.connect('users_db')
            
            # Call the original function, passing the connection as the first argument,
            # followed by any original arguments.
            result = func(conn, *args, **kwargs)
            return result
        except sqlite3.Error as e:
            print(f"Database error in '{func.__name__}': {e}", file=sys.stderr)
            return None
        except Exception as e:
            print(f"An unexpected error occured in '{func.__name__}': {e}", file=sys.stderr)
            return None
        finally:
            # Closes connection
            if conn:
                conn.close()
                print("Database clossed.", file=sys.stderr)
    return wrapper
    

@with_db_connection 
def get_user_by_id(conn, user_id):
    """
    Fetches a user from the 'users' table by ID using the provided connection.
    This function expects 'conn' as it's first argument, provided by the decorator.
    """
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
    return cursor.fetchone() 
    #### Fetch user by ID with automatic connection handling 

user = get_user_by_id(user_id=1)
print(user)