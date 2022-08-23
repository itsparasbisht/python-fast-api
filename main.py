from typing import Optional
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()

myPosts = [
    {
        "title": "post 1",
        "content": "this is an example",
        "id": 1
    },
    {
        "title": "what is up",
        "content": "hello hello hello",
        "id": 2
    }
]

# pydantic schema for Post
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

def find_post(id):
    for post in myPosts:
        if post["id"] == id:
            return post

# routes
@app.get("/")
async def root():
    return {"message": "Hello World!!"}

@app.get("/posts")
def get_posts():
    return {"data": myPosts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def set_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 10000)
    myPosts.append(post_dict)
    return {"data": post_dict}

@app.get('/posts/{id}')
def get_post(id: int):
    post = find_post(id)
    if not post:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    return {"data": post}