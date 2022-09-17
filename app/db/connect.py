from dotenv import dotenv_values
import psycopg2
from psycopg2.extras import RealDictCursor

config = dotenv_values(".env")

host = config["HOST"]
database = config["DATABASE"]
user = config["USER"]
dbPassword = config["DB_PASSWORD"]

def db_connect():
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password=dbPassword, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        
        return (conn, cursor)
    except Exception as error:
        print(f"DB Error: {error}")
        exit()