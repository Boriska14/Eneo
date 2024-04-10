from ast import List
import json
import re
from venv import logger
from fastapi import APIRouter, Depends
from psycopg2 import ProgrammingError
from sqlalchemy import Transaction, func
from sqlalchemy.orm import Session
from app.models import Donnees, EneoData
from app.routers.auth import get_db
from pydantic import ValidationError
from sqlalchemy import exc

from app.schemas import DonneesSchema



router = APIRouter()

@router.get("/data_by_date")
async def get_data_by_date(date: str = None, db: Session = Depends(get_db)):
    """
    Fetches EneoData records for a given date (without considering hour).

    Parameters:
        date (str, optional): Date in YYYY-MM-DD format. Defaults to None.
        db (Session): Database session object.

    Returns:
        List[EneoData]: List of EneoData objects.
    """

    if not date:
        return {"error": "Please provide a date in YYYY-MM-DD format."}

    date_column = func.left(EneoData.date, 10)
    query = db.query(EneoData).filter(date_column == date)

    results = await query.all()
    return results

def sum_kwh_from_query(query: List) -> float:
    total_kwh = 0.0
    for data in query:
        total_kwh += float(data.kwh)
    return total_kwh

def sum_montant_from_query(query: List) -> float:
    total_kwh = 0.0
    for data in query:
        total_kwh += float(data.montant)
    return total_kwh

"""
def inserer_donnees(db: Session, donnees: DonneesSchema):
    try:
        db_donnees = Donnees(**donnees.dict())
        db.add(db_donnees)
        db.commit()
        db.refresh(db_donnees)
        return db_donnees
    except ValidationError as e:
        # Gérer les erreurs de validation
        return None
"""

def inserer_donnees(db: Session, donnees: DonneesSchema):
    
    try:
        # Convertir l'objet DonneesSchema en un dictionnaire
        donnees_dict = donnees.dict()

        # Gérer la conversion de "NonRec_data_list" (supposant un format JSON)
        donnees_dict['NonRec_data_list'] = json.dumps(donnees_dict['NonRec_data_list'])

       
        db_donnees = Donnees(**donnees_dict)
        db.add(db_donnees)
        db.commit()
        db.refresh(db_donnees)

         
    except ProgrammingError as e:
        # Journaliser l'erreur pour le débogage
        logger.error("Erreur lors de l'insertion des données : %s", e)
        return None

    except Exception as e:
        # Gérer les erreurs inattendues
        logger.error("Erreur inattendue : %s", e)
        return None

def extract_lines(text):
  """
  Fonction pour extraire les lignes uniques entre accolades.
  """
  lines = []
  for match in re.finditer(r"\{(.*?)\}", text):
    lines.append(match.group(1))
  return lines
"""
def replace_commas(text):
  var=re.sub(r",(?=,)", "", text)
  return var
"""
def commas(text):
  var= re.sub(r"(?<=[\w])\,(?=[\w])", "", text)
  return var

def replace_commas(text):
  return re.sub(r",,,,,,", ":", text)

def remove(text):
   return re.sub(r",", "", text)

def convertir_tableau_objet(elements):
        
    structure_objet = {
    "pos": "Steal",
    "token": "",
    "montant": "",
    "kwh": "",
    "date": "",
    "meter_no": "",
    "num_ref": "",
    }

    objet = structure_objet.copy()

    for i in range(len(elements)):
    
        if i % 2 == 0:
            cle = elements[i]
                        
            if i==8:
                valeur= elements[9]+":"+elements[10]+":"+elements[11]
            else :  
                valeur = elements[i + 1]
            objet[cle] = valeur
            
    return objet

def convertir_tableau_en_objet(elements):
  
  if not elements or len(elements) % 2 != 0:
    return None

  structure_objet = {
      "pos": "Steal",
      "token": "",
      "montant": "",
      "kwh": "",
      "date": "",
      "meter_no": "",
      "num_ref": "",
  }

  objet = structure_objet.copy()

  for i in range(0, len(elements), 2):  # Iterate in steps of 2
    if i >= len(elements):
      break  # Break if we reach the end of the list
    cle = elements[i]

    # Handle missing elements or invalid structures based on key
    if cle in {"date", "meter_no", "num_ref"}:
      max_offset = 3
    else:
      max_offset = 1

    try:
      if i + max_offset < len(elements):
        # Construct value for keys with potentially multiple elements
        if cle == "date":
          valeur = ":".join(elements[i + 1:i + max_offset + 1])
        else:
          # Assign single element for other keys
          valeur = elements[i + 1]
        objet[cle] = valeur
    except IndexError:
      # Handle potential out-of-bounds errors gracefully
      return None

  return objet

