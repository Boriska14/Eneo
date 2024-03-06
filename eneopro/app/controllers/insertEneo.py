
from fastapi import UploadFile,File
from sqlalchemy.orm import Session
import pandas as pd
from sqlalchemy.orm import Session
from app.models import  EneoData
from app.schemas import EneoDataBase
from app.controllers import partner

def create_eneo_data(db: Session, eneo_data: EneoDataBase):
    db_eneo_data = EneoData(**eneo_data.dict())
    db.add(db_eneo_data)
    db.commit()
    db.refresh(db_eneo_data)
    return db_eneo_data

