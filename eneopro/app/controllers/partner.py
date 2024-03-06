from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Partner

from sqlalchemy.orm import Session
from app.routers.auth import get_db

from app.schemas import PartnerCreate, PartnerRequest



def get_partner(partner_request: PartnerRequest, db: Session = Depends(get_db)) :
    partner = db.query(Partner).filter(Partner.name == partner_request.name).first()
    return partner.id if partner else -1


def get_partner_by_id(db: Session, partner_id: int):
    return db.query(Partner).filter(Partner.id == partner_id).first()

def get_current_partner(db: Session, name: str):
    partner = get_partner(db, name)
    if not partner:
        return None
    return partner

def create_partner(partner_data: PartnerCreate, db: Session ):
    db_partner = Partner(name=partner_data.name, description=partner_data.description)
    db.add(db_partner)
    db.commit()
    db.refresh(db_partner)
    return db_partner


def delete_partner_by_name(db: Session, name: str):
    partner = db.query(Partner).filter(Partner.name == name).first()
    if partner:
        db.delete(partner)
        db.commit()
        return True
    return False

