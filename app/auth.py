
import logging
import urllib

from datetime import datetime, timedelta
from typing import Optional

import requests
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from app.models import User, UserInDB, Token, TokenData
from app.db import fake_users_db
from app.config import GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
import app.password



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    
    if not app.password.verify(password, user.hashed_password):
        return False
    
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=15)
    if expires_delta:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logging.info(payload)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: str = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTP_EXEPTION(status_code=400, detail="Inactive user")
    return current_user


# ROUTES
@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return form_data
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
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


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
    

@router.get('/github-login')
async def oauth_login():

    urlBase = 'https://github.com/login/oauth/authorize?'
    params = {
        "client_id": GITHUB_CLIENT_ID,
        "redirect_uri": "http://quickapi-jward3.cloudapps.unc.edu/oauth-callback",
        "scope": "user",
        "state": app.password.hash('farts')
    }

    return RedirectResponse(urlBase+urllib.parse.urlencode(params))
    # redirect user to urlBase+params
        

@router.post('/oauth-callback')
# not async b/c requests doesn't do async (https://github.com/tiangolo/astapi/issues/12#issuecomment-457706256)
def oauth_callback(code: str, state: str):
    urlBase = 'https://github.com/login/oauth/access_token'
    params = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code,
        "state": state
    }
    
    headers = {
        'Accept': 'application/json'
    }

    rsp = requests.post(urlBase, data=params, headers=headers)

    access_token = rsp.json()['access_token']
    

    api_headers = {'Authorization': 'token '+access_token}
    apiRsp = requests.get('https://api.github.com/user', headers=api_headers)

    return apiRsp.json()



    

    
    