import sqlite3
import functools
import sys
import time

def with_db_connection(func):
    """
    decorator that automatically handles opening and closing database connections,
    passes it as the first argument to the decorated function, and ensures the connetion is closed afterward.
    
    Args:
        func (callable): The function to be decorated.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            # Open the database connection
            conn = sqlite3.connect("users_db")

            # Call the original function, passing the connection as the first argument,
            # followed by any original arguments.
            result = func(conn, *args, **kwargs)
            return result
        except sqlite3.Error as e:
            print(f"Database error in '{func.__name__}': {e}", file=sys.stderr)
            return None
        except Exception as e:
            print(
                f"An unexpected error occured in '{func.__name__}': {e}",
                file=sys.stderr,
            )
            return None
        finally:
            # Closes connection
            if conn:
                conn.close()
                print("Database closed.", file=sys.stderr)

    return wrapper

# --- retry_on_failuire decorator ---
def retry_on_failure(retries=3, delay=2):
    """
    A decorator that retries a function if it raises and exception.

    Args:
        retries (int, opional): The maximum number of times to retrey the function. Defaults to 3.
        delay (int, optional): The delay in secons between retries. Defaults to 2.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for i in range(retries):
                try:
                    print(f"Attempt {i + 1}/{retries} for '{func.__name__}'...", file=sys.stderr)
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"Attempt {i + 1} failed for '{func.__name__}': {e}", file=sys.stderr)
                    if i < retries - 1:
                        print(f"Retrying in {delay} seconds...", file=sys.stderr)
                        time.sleep(delay)
                        
            print(f"All {retries} attempts failed for '{func.__name__}'.", file=sys.stderr)
            if last_exception:
                raise last_exception
            raise Exception(f"Function '{func.__name__}' failed after {retries} retries with no specific exception caught.")
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """
    Fetches all users from the database, with automatic retry on failure.

    Args:
        conn (sql.Connection): database connection
    """
    cursor = conn.cursor()
    # Simulates actual failure
    # if fetch_users_with_retry.counter < 2:
    #     fetch_users_with_retry.counter += 1
    #     raise sqlite3.OperationalError("Database is temporarily unavailble")
    
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# fetch_users_with_retry.counter = 0

users = fetch_users_with_retry()
print(users)