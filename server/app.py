from fastapi import FastAPI, APIRouter, Body, Request, Response, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from models.models import Base
from models.models import Shop as ShopModel  # SQLAlchemy Modell
from models.models import ShopCreate, ShopRead  # Pydantic Modelle
import time

app = FastAPI()

url = URL.create(
    drivername="postgresql",
    username="shopbuddy",
    password="shopbuddy",
    host="database",
    database="shopbuddy"
)


# Create the SQLAlchemy engine
engine = None
while engine is None:
    try:
        engine = create_engine(url)
        time.sleep(5)
    except Exception as e:
        print(f"Error creating engine: {e}")

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Dependency: Session-Objekt wird in jedem Request erstellt und nach Verwendung geschlossen
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/shops/", response_model=ShopRead)
def create_shop(shop: ShopCreate, db: Session = Depends(get_db)):
    # Prüfen, ob ein Shop mit demselben Namen bereits existiert
    existing_shop = db.query(ShopModel).filter(ShopModel.shop_name == shop.shop_name).first()
    if existing_shop:
        raise HTTPException(status_code=400, detail="Shop mit diesem Namen existiert bereits.")
    
    # Neuen Shop erstellen
    new_shop = ShopModel(shop_name=shop.shop_name)
    db.add(new_shop)
    db.commit()
    db.refresh(new_shop)  # Laden des neuen Shops aus der DB, um die ID zu erhalten
    
    return new_shop


'''
@app.post("/add/BonusProgram", response_description="Create a new Bonus Program", status_code=status.HTTP_201_CREATED, response_model=BonusProgramm)
def create_bonus_program(request: Request, program: BonusProgramm):
    db_model = program.getDBModel()

    db = SessionLocal()
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model

@app.get("/list")
async def list_fruits():
    db = SessionLocal()
    shops = db.query(Shop).all()
    return {"list": [{"_id": shop.id, "shop_name": shop.shop_name} for shop in shops]}

@app.post("/add/Shop", response_description="Create a new Shop", status_code=status.HTTP_201_CREATED, response_model=Shop)
def create_shop(request: Request, shop: Shop):
    db = SessionLocal()
    db.add(shop)
    db.commit()
    db.refresh(shop)
    return shop

@app.get("/listBonusPrograms")
async def list_bonus_programs():
    db = SessionLocal()
    bonus_programs = db.query(BonusProgramm_db_model).all()
    return {"list": [{"_id": program.id, "bonus_program_name": program.bonus_program_name} for program in bonus_programs]}

@app.post("/addCashbackProgram", response_description="Create a new Cashback Program", status_code=status.HTTP_201_CREATED, response_model=CashbackProgramm)
def create_cashback_program(request: Request, program: CashbackProgramm):
    db = SessionLocal()
    db.add(program)
    db.commit()
    db.refresh(program)
    return program

@app.get("/listCashbackPrograms")
async def list_cashback_programs():
    db = SessionLocal()
    cashback_programs = db.query(CashbackProgramm).all()
    return {"list": [{"_id": program.id, "shop_id": program.shop_id, "bonus_program_id": program.bonus_program_id, "cashbackrate": program.cashbackrate} for program in cashback_programs]}
'''