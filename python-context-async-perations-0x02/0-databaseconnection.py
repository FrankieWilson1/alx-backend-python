class DatabaseConnection:
    def __init__(self, db_name="my_database"):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
    
    def __enter__(self):
        self.connection = f"Connected to {self.db_name}"
        self.cursor = f"Cursor for {self.db_name}"
        print("Connection established")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"An exception of type {exc_type.__name__} occured: {exc_val}")
        else:
            print("No execption occured. Commiting Changes")
            
            # Simulate closing the connection
            print("Clossing the database connection.")
            self.connection = None
            self.cursor = None
            print("--- Exiting context: Connection closed ---")
            return False


# Using the context manager with the 'with' statement
print("\n-- Demonstrating DatabaseConnection context manager ---")
try:
    with DatabaseConnection("my_app_db") as db:
        print(f"Inside the 'with' block. Current DB object: {db}")
        print("Executing query: SELECT * FROM users")
        result = [
			{"id": 1, "name": "Alice", "email": "alice@example.com"},
			{"id": 2, "name": "Bob", "email": "bob@example.com"}
		]
        print("Query Results:")
        for row in result:
            print(row)
except ValueError as e:
    print(f"\nCaught an exception outside the 'with' block: {e}")