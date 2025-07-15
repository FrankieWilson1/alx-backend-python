import sqlite3
import functools
import sys

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


# --- transactional decorator ---
def transactional(func):
    """
    A decorator that wraps a database operation function within a transaction.
    If the decorated function raises an error, the transaction is rolled back;
    otherwise, it is commited.

    Args:
        func (callable): The function to be decorated.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not args or not isinstance(args[0], sqlite3.Connection):
            raise TypeError(
                f"Function '{func.__name__}' decorated with @transactional "
                "must recieve a sqlite3.Connection object as its first argument."
            )
            
        conn = args[0]
        try:
            result = func(*args, **kwargs)
            conn.commit()
            print(f"Transaction committed for '{func.__name__}'.", file=sys.stderr)
            return result
        except Exception as e:
            conn.rollback()
            print(f"Transaction rolled back for '{func.__name__}' due to error: {e}", file=sys.stderr)
            raise
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """
    Update a user's email. Its transaction and connection are managed by decorators.

    Args:
        conn (sqlite3.Connection): The database connection object.
        user_id (int ): The ID of the user whose email is to be updated.
        new_email (str): The new email address for the user.
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    print(f"Function 'update_user_email' executed query for user {user_id}.", file=sys.stderr)

#### Update user's email with automatic transaction handling
update_user_email(user_id=1, new_email='Craawford_cartwright@gmail.com')