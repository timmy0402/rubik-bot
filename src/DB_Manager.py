import pyodbc
import os 
from dotenv import load_dotenv
#loading database keys
load_dotenv()
server = os.getenv('AZURE_SQL_HOST')
database = os.getenv('AZURE_SQL_DATABASE')
username = os.getenv('AZURE_SQL_USERNAME')
password = os.getenv('AZURE_SQL_PASSWORD')
driver = os.getenv('{ODBC Driver 18 for SQL Server}')

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = pyodbc.connect(
            f'DRIVER={driver};SERVER=tcp:{server};PORT=1433;DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
        )
        self.cursor = self.connection.cursor()
        print('DB connected')

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print('DB connection closed')