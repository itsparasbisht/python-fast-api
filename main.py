from typing import Optional
from fastapi import FastAPI, status, HTTPException, Response
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

def find_index_post(id):
    for i, post in enumerate(myPosts):
        if post["id"] == id:
            return i

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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    return {"data": post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")

    myPosts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)