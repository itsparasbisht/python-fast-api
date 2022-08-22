from xmlrpc.client import Boolean
from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World!!"}

@app.get("/posts")
def get_posts():
    return {"data": "this is your post"}

@app.post("/post")
def set_post(payload: dict = Body(...)):
    print(payload)
    return {"new_post": f"title: {payload['title']}"}