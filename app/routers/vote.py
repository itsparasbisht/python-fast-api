from fastapi import status, Depends, HTTPException, Response, APIRouter

from .. import schemas, oauth2
from ..db.connect import db_connect

conn, cursor = db_connect()

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, current_user = Depends(oauth2.get_current_user)):
    user_id = str(current_user["id"])

    cursor.execute("SELECT * FROM votes WHERE post_id = %s AND user_id = %s", (str(vote.post_id), user_id))

    found_vote = cursor.fetchone()

    if vote.dir == 1:
        
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {user_id} has already voted on post {vote.post_id}")
        
        cursor.execute("""INSERT INTO votes (post_id, user_id) VALUES (%s, %s)""", (str(vote.post_id), user_id))

        conn.commit()

        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist")

        cursor.execute("DELETE FROM votes WHERE post_id = %s AND user_id = %s", (str(vote.post_id), user_id))

        conn.commit()
        return {"message": "successfully deleted vote"}
