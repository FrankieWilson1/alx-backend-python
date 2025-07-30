class ExecuteQuery:
    def __init__(self, query, params=None, db_name="my_database"):
        self.query = query
        self.params = params if params is not None else ()
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.result = []
    
    def __enter__(self):
        print(f"\n--- Entering context: Preparing to execute query ---")
        print(f"Connecting to {self.db_name}...")
        self.connection = f"Connected to {self.db_name}"
        self.cursor = f"Cursor for {self.db_name}"
        print("Connection and cursor ready.")
        
        print(f"Executing query: '{self.query}' with parameters: {self.params}")
        if "SELECT * FROM users WHERE age > ?" in self.query and self.params == (25,):
            self.result = [
			   {"id": 3, "name": "Charlie", "age": 20, "city": "Lagos"},
			   {"id": 4, "name": "John", "age": 15, "city": "Abuja"}
      		]
            print("Simulated query results fetched.")
        else:
            self.result = []
            print("No specific simulated results for this query or parameters")
        return self.result
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"An exception of type {exc_type.__name__} occured: {exc_val}")
            print("Rolling back transaction (simulated).")
        else:
            print("Query executed successfully. Committing changes (simulated).")
            
        print("Closing cursor and connection")
        self.cursor = None
        self.connection = None
        print("---Exiting context: Query execution complete and connection closed---")
        return False

query_to_run = "SELECT * FROM users WHERE age > ?"
parameter_val = 25

try:
    with ExecuteQuery(query_to_run, parameter_val) as user_data:
        print("\nResults from the 'with' block:")
        if user_data:
            for row in user_data:
                print(row)
        else:
            print("No users found matching the criteria.")
except Exception as e:
    print(f"\nCaught an unexpetect error outside the with block: {e}")

print("\n---Program finished---")
    
            