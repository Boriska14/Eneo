from datetime import datetime
from fastapi import APIRouter,Depends, Form, HTTPException
from app.database import engine
from sqlalchemy import and_, text
from app.models import EneoData,PartnerData
from sqlalchemy.orm import Session
from app.routers.auth import get_db
from sqlalchemy import func


router = APIRouter()

#COMPARAISON AVEC TOKEN
#route permettant de recuperer les données d'eneo qui ne trouvent pas de correspondance
#dans les données des partenaires et avec la date associer
@router.get("/rec_token")
async def get_rec_token(
    date: str = Form(),
    partner_name: str = Form(),
    skip: int = 0,
    db: Session = Depends(get_db),
) :
   
    query = db.query(EneoData)

    if date:
        date_column = func.left(EneoData.date, 10)
        query = query.filter(date_column == date)

    if partner_name:
        query = query.join(PartnerData, PartnerData.token == EneoData.token, isouter=True)

    query = query.filter(EneoData.pos == partner_name, PartnerData.token.is_(None)).offset(skip).all()
    return query

#route permettant de recuperer les données des partenaires qui ne trouvent pas de correspondance chez eneo
@router.get("/rec__token")
async def get_rec_token(
    date: str = Form(),
    partner_name: str = Form(),
    skip: int = 0,
    db: Session = Depends(get_db),
) :
   
    query = db.query(EneoData)

    if date:
        date_column = func.left(PartnerData.date, 10)
        query = query.filter(date_column == date)

    if partner_name:
        query = query.join(PartnerData, PartnerData.token == EneoData.token, isouter=True)

    query = query.filter(EneoData.pos == partner_name, EneoData.token.is_(None)).offset(skip).all()
    return query

"""
#COMPARAISON SANS TOKEN
@router.get("/rec")
async def get_rec(
    date: str = Form(),  # Explicitly allow None for date
    partner_name: str = Form(),  # Explicitly allow None for partner_name
    skip: int = 0,  # Use Form for skip parameter
    db: Session = Depends(get_db),
) :  # Indicate return type

    query = db.query(EneoData)

    if date:
        date_column = func.left(PartnerData.date, 10)
        query = query.filter(date_column == datetime.strptime(date,'%Y-%m-%d'))

    if partner_name:
        # Filter correctly based on the intended field
        query = query.filter(EneoData.pos == partner_name)

    # Join and filter based on meter_no, montant, and date, assuming NULL for missing PartnerData
        
    query = query.outerjoin(PartnerData,  onclause=and_(
        EneoData.meter_no == PartnerData.meter_no ,
        EneoData.montant == PartnerData.montant ,
        #EneoData.date == PartnerData.date,
        datetime.strptime(str(EneoData.date),"%Y-%m-%d %H:%M:%S") == datetime.strptime(str(PartnerData.date),'%d/%m/%Y %H:%M:%S'),),
        ).filter(PartnerData.meter_no.is_(None))

    return query.offset(skip).all()
"""

@router.get("/_rec")
def get_rec_token(skip: int = 0,partner_name:str=Form(), db: Session = Depends(get_db)):
    query = db.query(EneoData).join(
        PartnerData,
        EneoData.meter_no == PartnerData.meter_no and EneoData.montant == PartnerData.montant and EneoData.date == PartnerData.date,
        isouter=True,
    ).filter(EneoData.pos == partner_name, PartnerData.meter_no.is_(None)).offset(skip).all()
    return query 
