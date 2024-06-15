import mysql.connector
from mysql.connector import Error

def connect_to_database():
    try:
        # Replace the following details with your database information
        connection = mysql.connector.connect(
            host='locahost',  # e.g., 'localhost' or '127.0.0.1'
            database='user_identification',
            user='root',
            password='s@r@n1977'
        )
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Connected to MySQL Server version {db_info}")
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")

if __name__ == "__main__":
    connect_to_database()
