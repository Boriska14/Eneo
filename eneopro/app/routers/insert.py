from datetime import datetime
from fastapi import APIRouter, Body,  Form, HTTPException, Query,  UploadFile, File
import pandas as pd
from app.database import engine
from app.controllers import insert

router = APIRouter()

# Route pour traiter le fichier et insérer son contenu dans la base de données
@router.post("/process_and_insert_file/")
async def process_and_insert_file(partner_id:str=Form(), file:UploadFile=File(...)):
    # Lecture du fichier CSV avec pandas
    # Obtenir le contenu du fichier
    print("start")
    data = pd.read_csv(file.file, sep=";")
    data["date"]=insert.convert_date_format(data["date"])
    #data["date"] = data["date"].apply(convert_date_format)

    data["partner_id"]=partner_id
    #data.to_sql("partner_data",engine,if_exists='append',index=False,chunksize=10000 )
    print(data["date"])
    print("end")
   

    return {"message": "Le fichier a été traité et ses données ont été insérées dans la base de données avec succès."}

"""
@router.post("/process_and_insert_file/")
async def process_and_insert_file(partner_id: str = Form(...), file: UploadFile = File(...)):
    try:
        # Vérification de l'extension du fichier
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Le fichier doit être un fichier CSV")

        # Lecture du fichier CSV avec pandas
        data = pd.read_csv(file.file, sep=";")

        # Vérification de la présence des colonnes 'date' et 'compteur'
        if 'date' not in data.columns or 'compteur' not in data.columns:
            raise HTTPException(status_code=400, detail="Le fichier doit contenir des colonnes 'date' et 'compteur'")

        # Vérification de la taille du fichier (limitation à 5 Mo)
        file_size = len(file.file.read())
        if file_size > 5 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="La taille du fichier dépasse la limite autorisée (5 Mo)")

        # Conversion du format de la date
        data["date"] = insert.convert_date_format(data["date"])

        # Attribution d'un identifiant unique basé sur la date du fichier
        file_id = insert.generate_file_id(data["date"])

        # Association de l'identifiant unique au partenaire
        data["file_id"] = file_id
        data["partner_id"] = partner_id

        # Insertion des données dans la base de données
        data.to_sql("partner_data", engine, if_exists='append', index=False, chunksize=10000)

        return {"message": "Le fichier a été traité et ses données ont été insérées dans la base de données avec succès."}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
"""