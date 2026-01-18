import os
import database_utils as db_utils

# Define a test database file
TEST_DB = "test_database.db"

def test_database_operations():
    print("Testing database operations...")
    
    # 1. Create Connection
    conn = db_utils.create_connection(TEST_DB)
    if conn is not None:
        print("Connection successful.")
    else:
        print("Connection failed.")
        return

    # 2. Create Table
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    );
    """
    db_utils.create_table(conn, create_users_table)
    print("Table confirmed.")

    # 3. Create Record
    insert_user = "INSERT INTO users(name, email) VALUES(?, ?)"
    user_data = ("John Doe", "john@example.com")
    user_id = db_utils.create_record(conn, insert_user, user_data)
    print(f"User created with ID: {user_id}")

    # 4. Read Records
    select_users = "SELECT * FROM users"
    rows = db_utils.read_records(conn, select_users)
    print(f"Users found: {rows}")

    # 5. Update Record
    update_user = "UPDATE users SET name = ? WHERE id = ?"
    db_utils.update_record(conn, update_user, ("Jane Doe", user_id))
    
    updated_rows = db_utils.read_records(conn, select_users)
    print(f"Users after update: {updated_rows}")

    # 6. Delete Record
    delete_user = "DELETE FROM users WHERE id = ?"
    db_utils.delete_record(conn, delete_user, (user_id,))
    
    final_rows = db_utils.read_records(conn, select_users)
    print(f"Users after delete: {final_rows}")

    # 7. Close Connection
    db_utils.close_connection(conn)
    
    # Cleanup
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
        print("Test database removed.")

if __name__ == "__main__":
    test_database_operations()
