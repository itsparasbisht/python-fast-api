from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
import os

load_dotenv()

host = os.environ["HOST"]
database = os.environ["DATABASE"]
user = os.environ["USER"]
dbPassword = os.environ["DB_PASSWORD"]
port = os.environ["DB_PORT"]

print(host, database, user, dbPassword, port)

def db_connect():
    try:
        conn = psycopg2.connect(host='localhost', port=port, database='fastapi', user='postgres', password=dbPassword, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        
        return (conn, cursor)
    except Exception as error:
        print(f"DB Error: {error}")
        exit()