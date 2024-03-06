from sqlalchemy import Boolean, Column, Float, Integer, String, Enum,DateTime,ForeignKey
from app.database import Base
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