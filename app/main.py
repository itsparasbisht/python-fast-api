from fastapi import FastAPI
from .db import connect
from .routers import user, post, auth, vote

app = FastAPI()
db_res = connect.db_connect()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello World!"}
