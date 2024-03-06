import jwt
from datetime import datetime, timedelta
from jwt import PyJWTError
from typing import Optional
from fastapi import  HTTPException,Header
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models

SECRET_KEY = "secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    save_toke(db=SessionLocal(),username=data["sub"],token=encoded_jwt,expires_at=expire )
    return encoded_jwt

async def decode_token(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    token = authorization.split("Bearer ")[1]
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def save_toke(db:Session ,username:str,token:str, expires_at:datetime):
    db_token = models.Token(username=username, token=token , expires_at=expires_at)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token
