from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import connect
from .routers import user, post, auth, vote

origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_cerdentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

db_res = connect.db_connect()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello World!"}
