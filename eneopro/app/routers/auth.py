import re
from fastapi import APIRouter, Depends, Form, HTTPException, status
from pydantic import BaseModel, ValidationError, validator
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.controllers import auth
from app.schemas import UserDelete
from app.schemas import  UserCreate, UserLogin
from app.controllers.jwt import create_access_token ,decode_token
from typing import List
from app.controllers.auth import update_user
from app.schemas import UserUpdate



class User(BaseModel):
    username: str
    password: str
    role: str

class Partner(BaseModel):
    name:str
    description:str
    class Config:
        orm_mode=True

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/login/")
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    db_user = auth.get_current_user(db, username=login_data.username, password=login_data.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": db_user.username, "role": db_user.role})
    return {"access_token": access_token, "token_type": "bearer", "role":db_user.role}


"""@router.post("/register/")
def register_user(new_user: UserCreate, db: Session = Depends(get_db)):
    user = auth.get_user(db, new_user.username)   
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    return auth.create_user(db, new_user.username, new_user.password, new_user.role)"""

@router.post("/register/")
def register_user(new_user: UserCreate, db: Session = Depends(get_db)):
    # Validate the username
    try:
        new_user.validate_username(new_user.username)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    # Check if the username is already registered
    user = auth.get_user(db, new_user.username)   
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    return auth.create_user(db, new_user.username, new_user.password, new_user.role)

    

"""def login(login_data:UserLogin, db: Session = Depends(get_db)):
    user = auth.get_current_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    return {"username": user.username, "role": user.role}"""



@router.get("/protected/")
def protected_route(token: str = Depends(decode_token)):
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"message": "You have access to this protected route"}


@router.delete("/users/")
def delete_user(data: UserDelete, db: Session = Depends(get_db)):
    deleted = auth.delete_user_by_username(db, data.username)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"User {data.username} deleted successfully"}



@router.put("/users_update/", response_model=User)
def update_user_route(user_data: UserUpdate, user_id: int, db: Session = Depends(get_db)):
    db_user = update_user(db=db, user_id=user_id, user_data=user_data)
    if db_user:
        return db_user
    else:
        raise HTTPException(status_code=404, detail="User not found")
