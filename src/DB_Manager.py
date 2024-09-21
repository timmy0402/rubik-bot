import pyodbc
import os 
from dotenv import load_dotenv
#loading database keys
load_dotenv()
server = os.getenv('cubecrafterdb.database.windows.net')
database = os.getenv('cubeCrafterRecord')
username = os.getenv('CloudSA3c09cb3a')
password = os.getenv('G?ayhZ#X"j7i!Z5')
driver = os.getenv('{ODBC Driver 18 for SQL Server}')

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = pyodbc.connect(
            f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
        )
        self.cursor = self.connection.cursor()
        print('DB connected')

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print('DB connection closed')