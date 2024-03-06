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