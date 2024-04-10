from sqlalchemy import  JSON, Column, Float, Integer, String, Enum,DateTime,ForeignKey,TIMESTAMP,Text
from app.database import Base
from sqlalchemy.dialects.postgresql import ARRAY,VARCHAR  # Importez le type ARRAY depuis les dialectes PostgreSQL

from datetime import datetime


class UserRole(str, Enum):
    admin = "admin"
    user = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default=UserRole.user)

class Token(Base):
    __tablename__= "tokens"

    id=Column(Integer, primary_key=True, index=True)
    username=Column(String,index=True)
    token = Column(String,index=True)
    expires_at=Column(DateTime)

    def has_expired(self):
        return self.expire_at < datetime.utcnow()
    
class Partner(Base):
    __tablename__= "partners"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description=Column(String)


class PartnerData(Base):
    __tablename__ = "partner_data"

    id = Column(Integer, primary_key=True, index=True)
    meter_no = Column(String(255))
    nom_client = Column(String(255))
    num_client = Column(String(255))
    montant = Column(String)
    token = Column(String(20))
    date = Column(String(255))
    num_ref = Column(String(255))
    kwh = Column(String)
    status = Column(String)
    partner_id=Column(Integer,ForeignKey('partners.id'))



class EneoData(Base):
    __tablename__="eneo_data"

    pos=Column(String(255))
    token=Column(String(0),primary_key=True,unique=True)
    montant=Column(String)
    kwh=Column(String)
    date=Column(String)
    meter_no=Column(String(255))
    num_ref=Column(String(255))


class Logs(Base):
    __tablename__="log"


    id=Column(Integer,primary_key=True,autoincrement=True) 
    timestamp=Column(TIMESTAMP,nullable=False)
    level=Column(String(10),nullable=False)
    source=Column(String(50),nullable=False)
    message=Column(Text,nullable=False)
    context=Column(JSON)


class Donnees(Base):
    __tablename__ = 'donnees'

    id = Column(Integer, primary_key=True)
    date=Column(String)
    partner=Column(String)
    total= Column(String)
    total_montant = Column(Float)
    total_kwh = Column(Float)
    NonRec = Column(Integer)
    NonRec_montant = Column(Float)
    NonRec_kwh = Column(Float)
    Rec= Column(Integer)
    Rec_montant = Column(Float)
    Rec_kwh = Column(Float)
    NonRec_data_list = Column(ARRAY(VARCHAR))