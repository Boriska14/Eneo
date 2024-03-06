from typing import List
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.models import Partner
from app.routers.auth import get_db
from app.schemas import PartnerCreate, PartnerDelete, PartnerRequest
from app.controllers import partner
from fastapi import APIRouter, Depends
from app.schemas import PartnerCreate


router = APIRouter()


@router.post("/partners_create/")
def create_partner_route(partner_data: PartnerCreate, db: Session = Depends(get_db)):
    part = partner.get_current_partner(db,partner_data.name)
    if part:
        raise HTTPException(status_code=300,detail="partner already exist")
    return partner.create_partner(db=db, partner_data=partner_data)


@router.delete("/partners_delete/")
def delete_user(data: PartnerDelete, db: Session = Depends(get_db)):
    deleted = partner.delete_partner_by_name(db, data.name)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"User {data.name} deleted successfully"}


# Route pour récupérer les partenaires
@router.get("/partners/")
def get_partners(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Partner).offset(skip).limit(limit).all()
