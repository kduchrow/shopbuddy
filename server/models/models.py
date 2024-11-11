import uuid
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Boolean, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase
from datetime import date

from pydantic import BaseModel

class Base(DeclarativeBase):
    pass

### SQLAlchemy Modelle ###

class Shop(Base):
    __tablename__ = 'shop'
    
    shop_id = Column(Integer, primary_key=True, nullable=False)
    shop_name = Column(String(50), nullable=False)

    rel_shop_bonus = relationship('RelShopBonus', back_populates='shop')
    rel_referral = relationship('RelReferral', back_populates='shop')

class BonusProgram(Base):
    __tablename__ = 'bonusprogram'
    
    bonusprogram_id = Column(Integer, primary_key=True, nullable=False)
    bonusprogram_name = Column(String, nullable=False)
    is_cashback = Column(Boolean, nullable=False)
    is_discount = Column(Boolean, nullable=False)
    unit_name = Column(String)
    unit_abbr = Column(String)

    rel_shop_bonus = relationship('RelShopBonus', back_populates='bonusprogram')

class User(Base):
    __tablename__ = 'user'
    
    user_id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)

    rel_validity_confirmation = relationship('RelValidityConfirmation', back_populates='user')
    rel_referral = relationship('RelReferral', back_populates='user')

class RelShopBonus(Base):
    __tablename__ = 'rel_shop_bonus'
    
    rel_shop_bonus_id = Column(Integer, primary_key=True, nullable=False)
    shop_id = Column(Integer, ForeignKey('shop.shop_id'), nullable=False)
    bonusprogram_id = Column(Integer, ForeignKey('bonusprogram.bonusprogram_id'), nullable=False)
    bonus_rate = Column(Float, nullable=False)
    valid_from = Column(Date)
    valid_until = Column(Date)

    shop = relationship('Shop', back_populates='rel_shop_bonus')
    bonusprogram = relationship('BonusProgram', back_populates='rel_shop_bonus')
    rel_validity_confirmation = relationship('RelValidityConfirmation', back_populates='rel_shop_bonus')

class RelValidityConfirmation(Base):
    __tablename__ = 'rel_validity_confirmation'
    
    rel_shop_rate_valid_id = Column(Integer, primary_key=True, nullable=False)
    rel_shop_bonus_id = Column(Integer, ForeignKey('rel_shop_bonus.rel_shop_bonus_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    is_valid = Column(Boolean, nullable=False)
    comment = Column(String)
    confirmation_date = Column(Date, nullable=False)

    rel_shop_bonus = relationship('RelShopBonus', back_populates='rel_validity_confirmation')
    user = relationship('User', back_populates='rel_validity_confirmation')

class RelReferral(Base):
    __tablename__ = 'rel_referral'
    
    rel_referral_id = Column(Integer, primary_key=True, nullable=False)
    shop_id = Column(Integer, ForeignKey('shop.shop_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    link_or_code = Column(String)
    comment = Column(String)
    submit_date = Column(Date, nullable=False)

    shop = relationship('Shop', back_populates='rel_referral')
    user = relationship('User', back_populates='rel_referral')

### Pydantic Modelle ###

# Pydantic-Schemas für jedes SQLAlchemy-Modell
class ShopBase(BaseModel):
    shop_name: str

class ShopCreate(ShopBase):
    pass

class ShopRead(ShopBase):
    shop_id: int

    class Config:
        orm_mode = True

class BonusProgramBase(BaseModel):
    bonusprogram_name: str
    is_cashback: bool
    is_discount: bool
    unit_name: Optional[str] = None
    unit_abbr: Optional[str] = None

class BonusProgramCreate(BonusProgramBase):
    pass

class BonusProgramRead(BonusProgramBase):
    bonusprogram_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    user_id: int

    class Config:
        orm_mode = True

class RelShopBonusBase(BaseModel):
    bonus_rate: float
    valid_from: Optional[date]
    valid_until: Optional[date]

class RelShopBonusCreate(RelShopBonusBase):
    shop_id: int
    bonusprogram_id: int

class RelShopBonusRead(RelShopBonusBase):
    rel_shop_bonus_id: int
    shop_id: int
    bonusprogram_id: int

    class Config:
        orm_mode = True

class RelValidityConfirmationBase(BaseModel):
    is_valid: bool
    comment: Optional[str] = None
    confirmation_date: date

class RelValidityConfirmationCreate(RelValidityConfirmationBase):
    rel_shop_bonus_id: int
    user_id: int

class RelValidityConfirmationRead(RelValidityConfirmationBase):
    rel_shop_rate_valid_id: int
    rel_shop_bonus_id: int
    user_id: int

    class Config:
        orm_mode = True

class RelReferralBase(BaseModel):
    link_or_code: Optional[str] = None
    comment: Optional[str] = None
    submit_date: date

class RelReferralCreate(RelReferralBase):
    shop_id: int
    user_id: int

class RelReferralRead(RelReferralBase):
    rel_referral_id: int
    shop_id: int
    user_id: int

    class Config:
        orm_mode = True