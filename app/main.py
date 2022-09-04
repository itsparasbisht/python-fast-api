from typing import List, Optional
from fastapi import FastAPI, status, HTTPException, Response
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import schemas
from dotenv import dotenv_values

config = dotenv_values(".env")
dbPassword = config["DB_PASSWORD"]

app = FastAPI()

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

# routes
@app.get("/")
async def root():
    return {"message": "Hello World!!"}

@app.get("/posts", response_model=List[schemas.Post])
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def set_post(post: schemas.PostCreate):

    # %s to sanitize the data
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))

    new_post = cursor.fetchone()
    conn.commit()

    return new_post

@app.get('/posts/{id}', response_model=schemas.Post)
def get_post(id: int):

    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id)))
    posts = cursor.fetchone()

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    return posts

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}', response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate):

    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")

    return updated_post