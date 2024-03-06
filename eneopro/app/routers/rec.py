from fastapi import APIRouter,Depends
from app.database import engine
from sqlalchemy import text
from app.models import EneoData,PartnerData
from sqlalchemy.orm import Session
from app.routers.auth import get_db


router = APIRouter()

@router.get("/rec_token")
def get_rec_token(skip: int = 0, db: Session = Depends(get_db)):
    query = db.query(EneoData).join(PartnerData,PartnerData.token==EneoData.token,isouter=True).filter(EneoData.pos=='Orange',PartnerData.token.is_(None)).offset(skip).all()
    return query 

@router.get("/rec__token")
def get_rec_token(skip: int = 0,  db: Session = Depends(get_db)):
    query = db.query(EneoData).join(PartnerData,PartnerData.token==EneoData.token,isouter=True).filter(EneoData.pos=='Orange',EneoData.token.is_(None)).offset(skip).all()
    return query 

@router.get("/rec")
def get_rec_token(skip: int = 0, db: Session = Depends(get_db)):
    query = db.query(EneoData).join(PartnerData,PartnerData.meter_no==EneoData.meter_no,PartnerData.montant==EneoData.montant,PartnerData.date==EneoData.date,isouter=True).filter(EneoData.pos=='Orange',PartnerData.meter_no.is_(None)).offset(skip).all()
    return query 


@router.get("/_rec")
def get_rec_token(skip: int = 0, db: Session = Depends(get_db)):
    query = db.query(EneoData).join(PartnerData,PartnerData.meter_no==EneoData.meter_no,PartnerData.montant==EneoData.montant,PartnerData.date==EneoData.date,isouter=True).filter(EneoData.pos=='Orange',EneoData.meter_no.is_(None),EneoData.montant.is_(None),EneoData.date.is_(None)).offset(skip).all()
    return query 
