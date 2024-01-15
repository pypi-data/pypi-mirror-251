import sqlite3

def create_database(schema_file, database_name):
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(database_name)

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Read and execute SQL statements from the schema file
    with open(schema_file, 'r') as schema_file:
        schema_sql = schema_file.read()
        print(schema_sql)
        cursor.executescript(schema_sql)
        
    # Commit the changes
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

# Replace 'schema.sql' and 'your_database.db' with your actual schema file and desired database name
create_database('schema.sql', 'my_database.db')

