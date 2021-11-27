from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from auth import authenticate_user, create_access_token, get_current_active_user
from config.config import ACCESS_TOKEN_EXPIRE_MINUTES
from db.db_helper import create_db_user
from model.token import Token
from model.user import User


app = FastAPI()


@app.post("/user", status_code=status.HTTP_201_CREATED)
async def create_user(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    create_db_user(username, email, password)


@app.post("/oauth/token", response_model=Token)
async def get_login_access_token(oauth_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(oauth_data.username, oauth_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# FIXME: this should be same as `/oauth/token`. But Fastapi's oauth module doesn't support this.
# So I have to create another one to let user refresh token.
@app.post("/oauth/refresh_token")
async def refresh_token(oauth_data: OAuth2PasswordRequestForm = Depends()):
    pass


@app.post("/oauth/out")
async def logout_access_token(oauth_data: OAuth2PasswordRequestForm = Depends()):
    pass


@app.get("/user", response_model=User)
async def read_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user

