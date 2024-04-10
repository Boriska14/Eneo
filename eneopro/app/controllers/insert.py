from datetime import datetime
from fastapi import HTTPException, UploadFile,File
from sqlalchemy.orm import Session
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

async def convert_date_format(
  date_str: str
):
  """
  Fonction pour convertir une date et heure au format YYYY-MM-DD HH:MM:SS.

  Args:
    date_model: Modèle Pydantic contenant la date et l'heure à convertir (format d'origine).

  Returns:
    La date et l'heure au format YYYY-MM-DD HH:MM:SS.
  """

  try:
    # Conversion de la date et heure en objet datetime
    date = datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S")
    # Formatage de la date et heure au format YYYY-MM-DD HH:MM:SS
    return date.strftime("%Y-%m-%d %H:%M:%S")
  except ValueError:
    # Gestion des erreurs de format de date et heure
    raise HTTPException(
      status_code=422,
      detail="Le format de la date et heure est invalide. Veuillez utiliser le format DD/MM/YYYY HH:MM:SS.",
    )
