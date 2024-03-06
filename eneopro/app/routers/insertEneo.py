from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.routers.auth import get_db
from app.schemas import EneoDataBase
from app.controllers import insertEneo

router = APIRouter()

# Route pour traiter le fichier et insérer son contenu dans la base de données
@router.post("/insert_file/")
def process_and_insert_file( file:UploadFile=File(...), db: Session = Depends(get_db)):
    # Obtenir le contenu du fichier
    contents = file.file.read().decode("utf-8").splitlines()
    
    # Ignorer l'en-tête (première ligne)
    lines = contents[1:]

    # Lire chaque ligne du fichier
    for line in lines:
        # Diviser la ligne en colonnes (supposant qu'il s'agit d'un fichier CSV)
        columns = line.split("#")
 
        # Extraire les données pertinentes de la ligne
        pos = columns[0]
        token = columns[1]
        montant = columns[2]
        kwh = columns[3]
        date = columns[4]
        meter_no = columns[6]
        num_ref = columns[7]

        # Créer une instance de modèle de données appropriée
        eneo_data = EneoDataBase(pos=pos, token=token, montant=montant,
                                                  kwh=kwh, date=date,meter_no=meter_no, num_ref=num_ref)

        insertEneo.create_eneo_data(db=db,eneo_data=eneo_data)
        # Insérer cette instance dans la base de données
    
    return {"message": "Le fichier a été traité et ses données ont été insérées dans la base de données avec succès."}
