from fastapi import status, Depends, HTTPException, Response, APIRouter
from typing import List, Optional

from .. import schemas, oauth2
from ..db.connect import db_connect

conn, cursor = db_connect()

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/")
def get_posts(current_user = Depends(oauth2.get_current_user), limit: int = 10, search: Optional[str] = ""):

    key="%"+search+"%"

    # cursor.execute(""" SELECT posts.id, posts.title, posts.content, posts.published, posts.content, posts.created_at, posts.user_id, users.email FROM posts LEFT JOIN users ON posts.user_id = users.id WHERE posts.title ILIKE %s LIMIT(%s) """, (key, str(limit)))

    cursor.execute(""" select posts.*, users.email, count(votes.user_id) as likes from posts left join votes on
    posts.id = votes.post_id 
    left join users on 
    posts.user_id = users.id
    group by posts.id, users.email
    HAVING posts.title ILIKE %s limit(%s) """,
    (key, str(limit)))


    posts = cursor.fetchall()

    return posts

@router.post("/", status_code=status.HTTP_201_CREATED)
def set_post(post: schemas.PostCreate, current_user = Depends(oauth2.get_current_user)):
    user_id = current_user["id"]

    # %s to sanitize the data
    cursor.execute(""" INSERT INTO posts (title, content, published, user_id) VALUES (%s, %s, %s, %s) RETURNING * """, (post.title, post.content, post.published, user_id))

    new_post = cursor.fetchone()
    conn.commit()

    return new_post

@router.get('/{id}', response_model=schemas.Post)
def get_post(id: int, current_user = Depends(oauth2.get_current_user)):

    cursor.execute(" SELECT posts.id, posts.title, posts.content, posts.published, posts.created_at, posts.user_id, users.email FROM posts JOIN users ON posts.id = %s AND posts.user_id = users.id; ", (str(id),))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    return post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, current_user = Depends(oauth2.get_current_user)):

    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")

    if deleted_post["user_id"] != current_user["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, current_user = Depends(oauth2.get_current_user)):

    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")

    if updated_post["user_id"] != current_user["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")

    return updated_post