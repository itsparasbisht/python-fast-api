from fastapi import FastAPI
from .db import connect
from .routers import user, post

app = FastAPI()
db_res = connect.db_connect()

app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Hello World!"}
