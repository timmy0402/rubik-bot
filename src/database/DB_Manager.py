import pyodbc
import os
from dotenv import load_dotenv
import time
from paths import SRC_DIR
import logging

logger = logging.getLogger(__name__)

# loading database keys
load_dotenv(SRC_DIR / ".env")
server = os.getenv("AZURE_SQL_HOST")
database = os.getenv("AZURE_SQL_DATABASE")
username = os.getenv("AZURE_SQL_USERNAME")
password = os.getenv("AZURE_SQL_PASSWORD")
driver = os.getenv("{ODBC Driver 18 for SQL Server}")


class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        max_attempts = 3  # Maximum number of reconnection attempts
        for attempt in range(max_attempts):
            try:
                self.connection = pyodbc.connect(
                    f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER=tcp:{server};PORT=1433;DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=60;"
                )
                self.cursor = self.connection.cursor()
                self.cursor = self.connection.cursor()
                logger.info("DB connected")
                return  # Exit the function if successful
            except pyodbc.Error as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_attempts - 1:  # Don't wait on the last attempt
                    logger.info("Waiting for 5 seconds before retrying...")
                    time.sleep(5)

        if self.connection is None:
            logger.error("Error connecting to database after multiple attempts.")
            raise Exception("Unable to connect to the database.")

    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            if self.connection:
                self.connection.close()
            logger.info("DB connection closed")
        except pyodbc.Error as e:
            logger.error(f"Error closing database connection: {e}")

    def keep_alive(self):
        """Executes a lightweight query to keep the database connection alive."""
        if not self.cursor:
            logger.warning("No active cursor found. Attempting to reconnect.")
            self.connect()
        try:
            self.cursor.execute("SELECT 1")  # Simple query to keep the connection alive
            self.cursor.fetchall()  # Fetch results to complete the query execution
            logger.debug("Keep-alive query executed successfully.")
        except pyodbc.Error as e:
            logger.error(f"Error during keep-alive query: {e}")
            # Reconnect if the connection was lost
            self.connect()
