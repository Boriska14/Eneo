from fastapi import APIRouter,  Form, UploadFile, File
import pandas as pd
from app.database import engine

router = APIRouter()

# Route pour traiter le fichier et insérer son contenu dans la base de données
@router.post("/process_and_insert_file/")
def process_and_insert_file(partner_id:str=Form(), file:UploadFile=File(...)):
    # Lecture du fichier CSV avec pandas
    # Obtenir le contenu du fichier
    print("start")
    data = pd.read_csv(file.file, sep=";")
    data["partner_id"]=partner_id
    data.to_sql("partner_data",engine,if_exists='append',index=False,chunksize=10000 )
    print("end")
   
    return {"message": "Le fichier a été traité et ses données ont été insérées dans la base de données avec succès."}
