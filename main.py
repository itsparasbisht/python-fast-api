from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

# pydantic schema for Post
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# routes
@app.get("/")
async def root():
    return {"message": "Hello World!!"}

@app.get("/posts")
def get_posts():
    return {"data": "this is your post"}

@app.post("/post")
def set_post(post: Post):
    print(post)
    return {"data": post.dict()}