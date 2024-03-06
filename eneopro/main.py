from fastapi import FastAPI
from app.database import SessionLocal, engine, Base
from app.routers import auth,partner,upload,insert,insertEneo,rec
from fastapi.middleware.cors import CORSMiddleware
import app.schemas
import app.models

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(partner.router)
app.include_router(upload.router)
app.include_router(insert.router)
app.include_router(insertEneo.router)
app.include_router(rec.router)

# db = SessionLocal()

# create_user(db, "Karl Nyabe", "doudou", "user")

