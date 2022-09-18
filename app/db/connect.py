from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
import os

load_dotenv()

host = os.environ.get("HOST")
database = os.environ.get("DATABASE")
user = os.environ.get("USER")
dbPassword = os.environ.get("DB_PASSWORD")
port = os.environ.get("DB_PORT")

def db_connect():
    try:
        conn = psycopg2.connect(host='localhost', port=port, database='fastapi', user='postgres', password=dbPassword, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        
        return (conn, cursor)
    except Exception as error:
        print(f"DB Error: {error}")
        exit()