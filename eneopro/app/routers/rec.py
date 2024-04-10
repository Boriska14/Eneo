import json
from fastapi import APIRouter,Depends, Form, HTTPException
from app.controllers.rec import commas, convertir_tableau_en_objet, extract_lines, inserer_donnees, remove, replace_commas, sum_kwh_from_query, sum_montant_from_query
from app.database import engine
from sqlalchemy import Date, and_, text
from datetime import datetime
from fastapi import APIRouter,Depends, Form, HTTPException
from app.database import engine
from sqlalchemy import and_, text
from app.models import Donnees, EneoData,PartnerData
from sqlalchemy.orm import Session
from app.routers.auth import get_db
from sqlalchemy import func
from datetime import datetime
from sqlalchemy import cast, String
from sqlalchemy import func
import pandas as pd

from app.schemas import DonneesSchema, EneoDataBase



router = APIRouter()

#COMPARAISON AVEC TOKEN
#route permettant de recuperer les données d'eneo qui ne trouvent pas de correspondance
#dans les données des partenaires et avec la date associer
@router.post("/rec_token")
async def get_rec_token(
    date: str = Form(),
    partner_name: str = Form(),
    skip: int = 0,
    db: Session = Depends(get_db),
):

    data_list=[]
    data_start=[]
    query = db.query(EneoData)

    if date:
        date_column = func.left(EneoData.date, 10)
        query = query.filter(date_column == date)
        query_date=query.filter(EneoData.pos == partner_name)
       
    

    if partner_name:
        query = query.join(PartnerData, PartnerData.token == EneoData.token, isouter=True)

    query = query.filter(EneoData.pos == partner_name, PartnerData.token.is_(None)).offset(skip).all()


    for item in query:
        eneo_instance=EneoDataBase(
        pos=item.pos,
        token=item.token,
        kwh=item.kwh,
        date=item.date,
        montant=item.montant,
        meter_no=item.meter_no,
        num_ref=item.num_ref
        )
        data_list.append(eneo_instance)

    for item in query_date:
        data_start.append(item)

    number=len(data_list)
    total_kwh_list = sum_kwh_from_query(data_list)
    total_montant_list = sum_montant_from_query(data_list)

    start=len(data_start)

    total_kwh_start = sum_kwh_from_query(data_start)
    total_montant_start = sum_montant_from_query(data_start)


    nbr=start-number
    total_kwh_nbr=total_kwh_start-total_kwh_list
    total_montant_nbr=total_montant_start-total_montant_list

    data = DonneesSchema(
        date=date,
        partner=partner_name,
        total=start,
        total_montant=total_montant_start,
        total_kwh=total_kwh_start,
        NonRec=number,
        NonRec_montant=total_montant_list,
        NonRec_kwh=total_kwh_list,
        Rec=nbr,
        Rec_montant=total_montant_nbr,
        Rec_kwh=total_kwh_nbr,
        NonRec_data_list=data_list
    )
    inserer_donnees(db, data)

    return start,total_montant_start,total_kwh_start,nbr,total_montant_nbr,total_kwh_nbr,number,total_montant_list,total_kwh_list,data_list


@router.get("/details")
def get_details(date:str,partner:str,db: Session = Depends(get_db),):
    matching=db.query(Donnees.NonRec_data_list).filter(Donnees.date==date,Donnees.partner==partner).all()
    data = [row._asdict() for row in matching]
    json_data = json.dumps(data).replace("/", "").replace('"', "").replace(',',"").replace('\\',"").replace(" ",",")
    lines = extract_lines(json_data)
    new=[]

    for line in lines:
        details=[]    
        line=commas(line)
        line=replace_commas(line)
        line=remove(line)
        details.append(line)
        details[0] = details[0][20:]
        objet = convertir_tableau_en_objet(line.split(":"))
        if objet:  # Ajout uniquement si la conversion de l'objet est réussie
            new.append(objet)

    return new






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

    quer = db.query(PartnerData)

    if date:
        date_column = func.left(PartnerData.date, 10)
        quer= quer.filter(date_column == date_object)
    
    if partner_name:
        quer = quer.join(PartnerData, PartnerData.token == EneoData.token, isouter=True)

    quer = quer.filter(EneoData.pos == partner_name, EneoData.token.is_(None)).offset(skip).all()
    return quer


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



"""
#COMPARAISON SANS TOKEN
@router.get("/rec")
async def get_rec(
    date: str = Form(),  # Explicitly allow None for date
    partner_name: str = Form(),  # Explicitly allow None for partner_name
    skip: int = 0,  # Use Form for skip parameter
    db: Session = Depends(get_db),
) :  # Indicate return type
>>>>>>> f6c86196ba7ac8254c52074558eaec0f59ab38d5

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
