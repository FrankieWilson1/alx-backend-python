import sqlite3
import functools
import sys
import time

query_cache = {}    # Global cache for query result

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

# --- cache_query decorator---
def cache_query(func):
    """
    A decorator that caches the results of a database query based on the SQL query string
    to avoid redundant calls.
    Assumes the quer string is passed as the 'query' keyword or the second positianl arggument to the
    decorated function

    Args:
        func (function): The function to be decorated.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') # query from the keyword arguments
        
        if query is None and len(args) > 1:
            query = args[1]
            
        if query is None:
            raise ValueError("Cache_query decorator reuquires the SQL query string to be passed as a 'query' keyword argument or the second positional argument.")
        
        if query in query_cache:
            print(f"Cache hit or for query: '{query}'", file=sys.stderr)
            return query_cache[query]
        else:
            print(f"Cach miss for query: '{query}'. Executing query...", file=sys.stderr)
            result = func(*args, **kwargs)
            query_cache[query] = result
            return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users") 