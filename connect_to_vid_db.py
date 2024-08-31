import mysql.connector
from mysql.connector import Error

def get_db_connection():
    """Connect to the MySQL database and return the connection object."""
    # Database connection parameters
    db_name = "video_api_db"
    user = "root"
    password = "JonJamLil24!"
    host = "127.0.0.1"

    try:
        # Attempting to establish a connection
        conn = mysql.connector.connect(
            database=db_name,
            user=user,
            password=password,
            host=host
        )
        print("Connected to database!")
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None