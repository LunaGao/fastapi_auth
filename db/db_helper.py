from deta import Deta
from model.user_in_db import UserInDB
from passlib.context import CryptContext
from fastapi import HTTPException, status


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
deta = Deta()
db = deta.Base("fastapi_auth_db")


def create_db_user(username: str, email: str, form_password: str):
    user = db.get(username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_302_FOUND,
            detail="Username is already token.",
        )
    hashed_password = get_password_hash(form_password)
    db.put({
        "username": username,
        "full_name": username,
        "email": email,
        "hashed_password": hashed_password,
        "disabled": False,
    }, username)


def get_user(username: str):
    user = db.get(username)
    if user:
        return UserInDB(**user)
    return None


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)
