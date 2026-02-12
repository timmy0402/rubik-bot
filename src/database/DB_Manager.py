import pyodbc
import os
from dotenv import load_dotenv
import time
from paths import SRC_DIR
import logging

logger = logging.getLogger(__name__)

# Load database environment variables from .env file
load_dotenv(SRC_DIR / ".env")
if(os.getenv("ENV", "").upper() == "PROD"):
    logger.info("Running in production environment. Loading production database credentials.")
    server = os.getenv("AZURE_SQL_HOST")
    database = os.getenv("AZURE_SQL_DATABASE")
    username = os.getenv("AZURE_SQL_USERNAME")
    password = os.getenv("AZURE_SQL_PASSWORD")
    driver = "{ODBC Driver 18 for SQL Server}"
    trust = "no"
else:
    logger.info("Running in development environment. Loading development database credentials.")
    server = os.getenv("DEV_SQL_HOST")
    database = os.getenv("DEV_SQL_DATABASE")
    username = os.getenv("DEV_SQL_USERNAME")
    password = os.getenv("DEV_SQL_PASSWORD")
    password = "{" + password + "}"
    driver = "{ODBC Driver 18 for SQL Server}"
    trust = "yes"

class DatabaseManager:
    """
    Manages connections and operations for the Azure SQL Database.
    Handles connection lifecycle, reconnection logic, and keep-alive tasks.
    """

    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        Establishes a connection to the Azure SQL Database.
        Includes retry logic and checks for existing active connections.
        """
        # Check if we already have an active connection
        if self.connection and self.cursor:
            try:
                self.cursor.execute("SELECT 1")
                return
            except pyodbc.Error:
                logger.info("Connection lost, reconnecting...")
                self.close()

        max_attempts = 3  # Maximum number of reconnection attempts
        for attempt in range(max_attempts):
            try:
                # Construct connection string and connect
                self.connection = pyodbc.connect(
                    f"DRIVER={driver};SERVER=tcp:{server};PORT=1433;DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate={trust};Connection Timeout=60;"
                )
                self.cursor = self.connection.cursor()
                logger.info("DB connected successfully")
                return
            except pyodbc.Error as e:
                logger.warning(f"Connection attempt {attempt + 1} failed: {e}")
                if attempt < max_attempts - 1:
                    logger.info("Waiting for 5 seconds before retrying...")
                    time.sleep(5)

        if self.connection is None:
            logger.error("Failed to connect to database after multiple attempts.")
            raise Exception("Unable to connect to the database.")

    def close(self):
        """
        Safely closes the database cursor and connection.
        """
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            logger.info("DB connection closed")
        except pyodbc.Error as e:
            logger.error(f"Error closing database connection: {e}")
        finally:
            self.cursor = None
            self.connection = None

    def keep_alive(self):
        """
        Executes a lightweight query to keep the database connection alive.
        Prevents Azure SQL from timing out idle connections.
        """
        if not self.cursor:
            logger.warning("No active cursor found. Attempting to reconnect.")
            self.connect()
        try:
            self.cursor.execute("SELECT 1")
            self.cursor.fetchall()
            logger.debug("Keep-alive query executed successfully.")
        except pyodbc.Error as e:
            logger.error(f"Error during keep-alive query: {e}")
            # Reconnect if the connection was lost
            self.connect()