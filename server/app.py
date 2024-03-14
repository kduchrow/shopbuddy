
from fastapi import FastAPI, APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient
import pandas as pd

from models.models import Shop

app = FastAPI()

client = MongoClient("mongo", 27017)
db = client.test_database
collection = db.test_collection

p_cols = ['island', 'bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g', 'sex']

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/add/{my_fruit}")
async def get_fruits(my_fruit: str):
    return {"fruit": str(collection.insert_one({"fruit": my_fruit}).inserted_id)}

@app.get("/list")
async def list_fruits():
    return {"list": list(collection["shop"].find({}, {"_id": False}))}


@app.post("/", response_description="Create a new Shop", status_code= status.HTTP_201_CREATED, response_model=Shop)
def create_shop(request: Request, shop: Shop):
    shop = jsonable_encoder(shop)
    new_shop = collection["shop"].insert_one(shop)
    created_shop = collection["shop"].find_one(
        {"_id": new_shop.inserted_id}
    )

    return created_shop
