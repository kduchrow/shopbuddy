import uuid
from sqlalchemy import Column, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Shop(Base):
    __tablename__ = 'shops'

    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))
    shop_name = Column(String(255), nullable=False)

class BonusProgramm(Base):
    __tablename__ = 'bonus_programs'

    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))
    bonus_program_name = Column(String(255), nullable=False)

class CashbackProgramm(Base):
    __tablename__ = 'cashback_programs'

    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))
    bonus_program_id = Column(String(36), nullable=False)
    shop_id = Column(String(36), nullable=False)
    cashbackrate = Column(Float, nullable=False)
