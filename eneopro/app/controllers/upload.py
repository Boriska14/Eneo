from datetime import datetime
import os
from uuid import uuid4


UPLOADS_DIR = "./uploads"

def create_upload_dir():
    if not os.path.exists(UPLOADS_DIR):
        os.makedirs(UPLOADS_DIR)

def generate_unique_filename(filename):
    unique_id = uuid4().hex
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{timestamp}_{unique_id}_{filename}"