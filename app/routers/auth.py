from fastapi import status, Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from ..db.connect import db_connect
from .. import schemas, utils, oauth2

conn, cursor = db_connect()

router = APIRouter(
    tags = ["Authentication"]
)

@router.post('/login', response_model=schemas.Token)
def login(user_creds: OAuth2PasswordRequestForm = Depends()):

    cursor.execute("""SELECT * FROM users WHERE email = %s""", (user_creds.username,))
    user = cursor.fetchone()
    conn.commit()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(user_creds.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create token for valid user
    access_token = oauth2.create_access_token(data={"user_id": user["id"]})
    return {"access_token": access_token, "token_type": "bearer"}

    
    
