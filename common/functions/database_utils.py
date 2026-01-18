import sqlite3
from sqlite3 import Error
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_connection(db_file):
    """ 
    Create a database connection to the SQLite database specified by db_file.
    If the database does not exist, it will be created.
    
    :param db_file: database file path
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        logging.info(f"Connected to SQLite database: {db_file}")
        return conn
    except Error as e:
        logging.error(f"Error connecting to database: {e}")
    
    return conn

def create_table(conn, create_table_sql):
    """ 
    Create a table from the create_table_sql statement
    
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        logging.info("Table created successfully")
    except Error as e:
        logging.error(f"Error creating table: {e}")

def create_record(conn, sql, params):
    """
    Create a new record into the table
    
    :param conn: Connection object
    :param sql: INSERT statement
    :param params: tuple of values
    :return: last row id
    """
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        logging.info(f"Record created successfully with ID: {cur.lastrowid}")
        return cur.lastrowid
    except Error as e:
        logging.error(f"Error creating record: {e}")
        return None

def read_records(conn, sql, params=None):
    """
    Query all rows in the table
    
    :param conn: Connection object
    :param sql: SELECT statement
    :param params: tuple of values (optional)
    :return: list of rows
    """
    try:
        cur = conn.cursor()
        if params:
            cur.execute(sql, params)
        else:
            cur.execute(sql)
        rows = cur.fetchall()
        return rows
    except Error as e:
        logging.error(f"Error reading records: {e}")
        return []

def update_record(conn, sql, params):
    """
    Update a record in the table
    
    :param conn: Connection object
    :param sql: UPDATE statement
    :param params: tuple of values
    :return: number of rows updated
    """
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        logging.info(f"Updated {cur.rowcount} row(s)")
        return cur.rowcount
    except Error as e:
        logging.error(f"Error updating record: {e}")
        return 0

def delete_record(conn, sql, params):
    """
    Delete a record from the table
    
    :param conn: Connection object
    :param sql: DELETE statement
    :param params: tuple of values
    :return: number of rows deleted
    """
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        logging.info(f"Deleted {cur.rowcount} row(s)")
        return cur.rowcount
    except Error as e:
        logging.error(f"Error deleting record: {e}")
        return 0

def close_connection(conn):
    """
    Close the database connection
    
    :param conn: Connection object
    """
    if conn:
        conn.close()
        logging.info("Database connection closed")
