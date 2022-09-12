from fastapi import status, Depends, HTTPException, Response, APIRouter
from typing import List

from .. import schemas, oauth2
from ..db.connect import db_connect

conn, cursor = db_connect()

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.Post])
def get_posts(current_user = Depends(oauth2.get_current_user)):
    # print(dict(current_user))

    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def set_post(post: schemas.PostCreate, current_user = Depends(oauth2.get_current_user)):

    # %s to sanitize the data
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))

    new_post = cursor.fetchone()
    conn.commit()

    return new_post

@router.get('/{id}', response_model=schemas.Post)
def get_post(id: int, current_user = Depends(oauth2.get_current_user)):

    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id)))
    posts = cursor.fetchone()

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    return posts

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, current_user = Depends(oauth2.get_current_user)):

    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, current_user = Depends(oauth2.get_current_user)):

    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")

    return updated_post