
from fastapi import UploadFile,File
from sqlalchemy.orm import Session
import pandas as pd
from sqlalchemy.orm import Session
from app.models import  PartnerData
from app.schemas import PartnerDataBase
from app.controllers import partner

def create_partner_data(db: Session, partner_data: PartnerDataBase):
    db_partner_data = PartnerData(**partner_data.dict())
    db.add(db_partner_data)
    db.commit()
    db.refresh(db_partner_data)
    return db_partner_data
