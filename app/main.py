from fastapi import FastAPI
from .db import connect
from .routers import post, user

app = FastAPI()
db_res = connect.db_connect()

if not db_res:
    print("Database connection failed")
else:
    cursor, conn = list(db_res)

def db_get():
    return cursor, conn

app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Hello World!"}
