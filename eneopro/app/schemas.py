
from pydantic import BaseModel, Field,constr, validator
from fastapi import UploadFile,File
import re

from app.models import EneoData


class UserBase(BaseModel):
    username: constr(pattern="^[a-zA-Z]+\.[a-zA-Z]+$") # type: ignore
    @validator('username')
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z]+\.[a-zA-Z]+$', v):
            raise ValueError('Le nom d\'utilisateur doit être au format "prenom.nom"')
        return v


class UserCreate(UserBase):
    password: str
    role: str = Field(..., min_length=1)

class UserLogin(UserBase):
    password: str

class UserDelete(BaseModel):
    username: str


class UserUpdate(BaseModel):
    username: str
    password: str
    role:str



class PartnerCreate(BaseModel):
    name: str
    description: str

class PartnerDelete(BaseModel):
    name: str

class InsertData(BaseModel):
    partner_id:int
    file: UploadFile = File(...)
    
class PartnerRequest(BaseModel):
    name: str


class PartnerDataBase(BaseModel):
    meter_no: str
    nom_client: str
    num_client: str
    montant: str
    token: str
    date: str
    num_ref: str
    kwh: str
    status: str
    partner_id:str

class EneoDataBase(BaseModel):
    pos:str
    token:str
    montant:str
    kwh:str
    date:str
    meter_no:str
    num_ref:str

   
class DateModel(BaseModel):
  date_str: str


class DonneesSchema(BaseModel):
    date: str
    partner: str
    total: int
    total_montant: float
    total_kwh: float
    NonRec: int
    NonRec_montant: float
    NonRec_kwh: float
    Rec: int
    Rec_montant: float
    Rec_kwh: float
    NonRec_data_list: list[EneoDataBase]  # Assurez-vous que le type de données est approprié
