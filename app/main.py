from fastapi import FastAPI, Depends, HTTPException, APIRouter
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer

import auth
from infrastructure.dbsession import SessionLocal

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get('/')
async def root():
    return RedirectResponse('/login')

@app.get('/test/db')
async def test_db():
    session = SessionLocal()
    return session


@app.get('/secured-endpoint')
async def secured_endpoint(token: str = Depends(oauth2_scheme)):
    return {'message': "You got in with the token"}

app.include_router(auth.router, tags=["auth"])