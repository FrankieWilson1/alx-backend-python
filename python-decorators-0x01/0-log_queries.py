import sqlite3
import functools
import sys
from datetime import datetime

#### decorator to lof SQL queries
""" YOUR CODE GOES HERE"""

def log_queries(func):
    """
    A decorator that logs the SQL query being executed by the decorated function.
    Assumes the SQL query is passed as the first positional argument or a keyword
    argument named 'query'
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query_to_log = None
        # Determine the query argument.
        if "query" in kwargs:
            query_to_log = kwargs["query"]
        elif args:
            # Assuming the first positional argument is the query
            query_to_log = args[0]
            
        start_time = datetime.now()

        if query_to_log:
            # Logs the query before execution
            print(f"[{start_time.strftime('%Y-%m-%d %H:%M:%S')}] Executing SQL Query: '{query_to_log}'", file=sys.stdout)
        else:
            # Handles cases where the query argument might not be found
            print(
                f"[{start_time.strftime('%Y-%m-%d %H:%M-%S')}] Warning: No identifiable query argument found ofr function '{func.__name__}'",
                file=sys.stderr,
            )

        results = func(*args, **kwargs)
        endtime = datetime.now()
        execute_time = endtime - start_time
        
        print(f"[{endtime.strftime('%Y-%m-%d %H:%M:%S')}] Qury completed in {execute_time.total_seconds():.4f} secons.", file=sys.stdout)
        return results

    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect("users_db")
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
