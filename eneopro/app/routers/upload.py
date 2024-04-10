from fastapi import APIRouter, UploadFile,File
import shutil
import os 
from app.controllers.upload import create_upload_dir,generate_unique_filename,UPLOADS_DIR

router = APIRouter()


@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    create_upload_dir()
    unique_filename = generate_unique_filename(file.filename)
    file_location = os.path.join(UPLOADS_DIR, unique_filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": unique_filename}

"""
UPLOADS_DIR = "uploads"  # Dossier de stockage des fichiers uploadés

def create_upload_dir():
    if not os.path.exists(UPLOADS_DIR):
        os.makedirs(UPLOADS_DIR)

def generate_unique_filename(original_filename: str) -> str:
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{current_time}_{original_filename}"

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Vérification de la taille du fichier (10 Mo maximum)
    max_file_size = 10 * 1024 * 1024  # 10 Mo en octets
    if file.content_length > max_file_size:
        raise HTTPException(status_code=413, detail="La taille du fichier dépasse la limite autorisée (10 Mo).")

    create_upload_dir()
    unique_filename = generate_unique_filename(file.filename)
    file_location = os.path.join(UPLOADS_DIR, unique_filename)

    # Enregistrement du fichier sur le serveur
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": unique_filename}
"""