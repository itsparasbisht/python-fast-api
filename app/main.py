import imp
from typing import Optional
from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from dotenv import dotenv_values

config = dotenv_values(".env")
dbPassword = config["DB_PASSWORD"]

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

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password=dbPassword, cursor_factory=RealDictCursor)

        cursor = conn.cursor()
        print("Database connection made!")
        break
    except Exception as error:
        print("Database connection failed!")
        print("Error: ", error)
        time.sleep(2)

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
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def set_post(post: Post):

    # %s to sanitize the data
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))

    new_post = cursor.fetchone()
    conn.commit()

    return {"data": new_post}

@app.get('/posts/{id}')
def get_post(id: int):

    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id)))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    return {"data": post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")

    post_dict = post.dict()
    post_dict['id'] = id
    myPosts[index] = post_dict
    return {"data": post_dict}