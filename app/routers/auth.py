from fastapi import status, HTTPException, APIRouter

from ..db.connect import db_connect
from .. import schemas, utils, oauth2

conn, cursor = db_connect()

router = APIRouter(
    tags = ["Authentication"]
)

@router.post('/login')
def login(user_creds: schemas.UserLogin):

    cursor.execute("""SELECT * FROM users WHERE email = %s""", (user_creds.email,))
    user = cursor.fetchone()
    conn.commit()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if not utils.verify(user_creds.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    # create token for valid user
    access_token = oauth2.create_access_token(data={"user_id": user["id"]})
    return {"access_token": access_token, "token_type": "bearer"}

    
    
