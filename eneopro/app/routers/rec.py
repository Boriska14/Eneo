from fastapi import APIRouter,Depends, Form, HTTPException
from app.database import engine
from sqlalchemy import Date, and_, text
from app.models import EneoData,PartnerData
from sqlalchemy.orm import Session
from app.routers.auth import get_db
from sqlalchemy import func
from datetime import datetime
from sqlalchemy import cast, String
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
):

    query = db.query(EneoData)
    data_list = []

    if date:
        date_column = cast(EneoData.date, String(10))
        query = query.filter(date_column == date)

    if partner_name:
        query = query.join(PartnerData, PartnerData.token == EneoData.token, isouter=True)

    query = query.filter(EneoData.pos == partner_name, PartnerData.token.is_(None)).offset(skip).all()

    for item in query:
        data_list.append(item)

    number=len(data_list)
    return number,data_list


#route permettant de recuperer les données des partenaires qui ne trouvent pas de correspondance chez eneo
@router.get("/rec__token")
async def get_rec_token(
    date: str = Form(),
    partner_name: str = Form(),
    skip: int = 0,
    db: Session = Depends(get_db),
) :
   

    format_str = "%Y-%m-%d"
    date_object = datetime.strptime(date, format_str).strftime("%d/%m/%Y")
    print(date_object)

    query = db.query(EneoData)

    if date:
        date_column = func.left(PartnerData.date, 10)
        query = query.filter(date_column == date_object)

    if partner_name:
        query = query.join(PartnerData, PartnerData.token == EneoData.token, isouter=True)

    query = query.filter(EneoData.pos == partner_name, EneoData.token.is_(None)).offset(skip).all()
    return query


#COMPARAISON SANS TOKEN
@router.get("/rec")
async def get_rec(
    date: str = Form(None),  # Allow None for date
    partner_name: str = Form(None),  # Allow None for partner_name
    skip: int = Form(0),  # Use Form for skip parameter
    db: Session = Depends(get_db),
):

   
    query = db.query(EneoData)

    if date:
        query = query.filter(EneoData.date == date)

    if partner_name:
        query = query.filter(EneoData.pos == partner_name)

    query = query.outerjoin(PartnerData, onclause=and_(
        EneoData.meter_no == PartnerData.meter_no,
        EneoData.montant == PartnerData.montant,
        cast(EneoData.date, Date) == cast(PartnerData.date, Date)  # Assuming Date is the appropriate timestamp type
    )).filter(PartnerData.meter_no.is_(None))

    return query.offset(skip).all()




@router.get("/_rec")
def get_rec_token(skip: int = 0,partner_name:str=Form(), db: Session = Depends(get_db)):
    query = db.query(EneoData).join(
        PartnerData,
        EneoData.meter_no == PartnerData.meter_no and EneoData.montant == PartnerData.montant and EneoData.date == PartnerData.date,
        isouter=True,
    ).filter(EneoData.pos == partner_name, PartnerData.meter_no.is_(None)).offset(skip).all()
    return query 
