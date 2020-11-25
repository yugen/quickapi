
import logging
import urllib

from datetime import datetime, timedelta
from typing import Optional

import requests
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from models import User, UserInDB, Token, TokenData
from db import fake_users_db
from config import GITHUB_CLIENT_ID, \
                        GITHUB_CLIENT_SECRET, \
                        SECRET_KEY, \
                        ALGORITHM, \
                        ACCESS_TOKEN_EXPIRE_MINUTES, \
                        ORCID_CLIENT_ID, \
                        ORCID_CLIENT_SECRET, \
                        BASE_URL
import password

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
    

@router.get('/login')
async def login_links():
    return HTMLResponse('<html><body><ul><li><a href="/github-login">Login w/ github</a></li><li><a href="/orcid-login">Login w/ orcid</a></li></ul></body></html>')

@router.get('/github-login')
async def github_login():

    urlBase = 'https://github.com/login/oauth/authorize?'
    params = {
        "client_id": GITHUB_CLIENT_ID,
        "redirect_uri": BASE_URL+"oauth-callback",
        "scope": "user",
        "state": app.password.hash('farts')
    }

    return RedirectResponse(urlBase+urllib.parse.urlencode(params))
    # redirect user to urlBase+params
        

@router.post('/oauth-callback')
# not async b/c requests doesn't do async (https://github.com/tiangolo/astapi/issues/12#issuecomment-457706256)
def github_callback(code: str, state: str):
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


@router.get('/orcid-login')
async def orcid_login():
    urlBase = 'https://orcid.org/oauth/authorize?'
    params = {
        "client_id": ORCID_CLIENT_ID,
        "response_type": "code",
        # "scope": "/read-public",
        "scope": "/authenticate",
        "redirect_uri": BASE_URL+'orcid-callback'
    }

    return RedirectResponse(urlBase+urllib.parse.urlencode(params))


# @router.post('/orcid-callback')
@router.get('/orcid-callback')
# not async b/c requests doesn't do async (https://github.com/tiangolo/astapi/issues/12#issuecomment-457706256)
def orcid_callback(code: str):
    urlBase = 'https://orcid.org/oauth/token'
    params = {
        "client_id": ORCID_CLIENT_ID,
        "client_secret": ORCID_CLIENT_SECRET,
        "grant_type": 'authorization_code',
        "code": code
    }

    rsp = requests.post(urlBase, data=params)

    auth_dict = rsp.json()

    access_token = auth_dict.get('access_token')
    orcid_id = auth_dict.get('orcid')
    if not access_token:
        raise PermissionError('Failed to authenticate.  No access token in response')
    
    logging.debug('testing debug: getting record_dict');
    logging.info('testing info: getting record_dict');
    logging.warning('testing warning: getting record_dict');
    logging.error('testing error: getting record_dict');
    record_dict = fetch_public_orcid_record(access_token, orcid_id)

    return {"auth": auth_dict, "record": record_dict}

def fetch_public_orcid_record(access_token: str, orcid_id: str):
    logging.warning('param access_token: '+access_token)
    logging.warning('param orchid_id: '+orcid_id)

    api_headers = {
        'Authorization type': 'bearer',
        'Access token': access_token,
    }
    record_url = 'https://api.sandbox.orcid.org/v2.1/%s/record' % orcid_id

    logging.warning('record_url:'+record_url)
    logging.warning('access_token:'+access_token)
    
    rcd_rsp = requests.get(record_url, headers=api_headers)
    if rcd_rsp.status_code != 200:
        logging.error(rcd_rsp)
        return {'message': 'got response '+str(rcd_rsp.status_code)+' with message: '+rcd_rsp.text}

    try:
        record_dict = rcd_rsp.json()
    except Error as e:
        logging.error(e)
        return {'rcd_rsp.text': rcd_rsp.text}
