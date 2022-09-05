from fastapi import status, HTTPException, APIRouter
from .. import schemas, utils
from ..db.connect import db_connect

conn, cursor = db_connect()
router = APIRouter()

router = APIRouter()

@router.post('/user', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate):

    # hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    cursor.execute("""INSERT INTO users (email, password) VALUES (%s, %s) RETURNING *""", (user.email, user.password))
    new_user = cursor.fetchone()
    conn.commit()

    return new_user

@router.get('/user/{id}', status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(id: int):

    cursor.execute(f" SELECT * FROM users WHERE id = {id}")
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} does not exist")

    return user