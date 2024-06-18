from fastapi import FastAPI, UploadFile, HTTPException, Request
from pathlib import Path
from typing import List
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, select, insert, update, delete, func
import base64

from app.db_model import *
from app.api_communication import api_patch
from app.yolo_nas import YOLO
from app.file_control import save_file

BASE_DIR = Path(__file__).resolve().parent

engine = create_engine('sqlite:///spark.db')
metadata = MetaData()
parkinglots = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String),
              Column('image', String, default="NULL"),
              Column('cnt', Integer, default=0))
metadata.create_all(engine)

app = FastAPI()


# 라즈베리파이에서 보내는 요청
yolo = YOLO()
@app.patch("/photo/{idx}")
async def detection(file: UploadFile, idx: int):
    try:
        path = await save_file(file.file)
        car = await yolo.count_car(path, idx)
        with engine.connect() as conn:
            with open(f'predicted{idx}.jpg', 'rb') as image_file:
                encoded_image = base64.b64encode(image_file.read())
                update_stmt = (
                update(parkinglots)
                .where(parkinglots.c.id == idx)
                .values(image=encoded_image, cnt=car))
            result = conn.execute(update_stmt)
            conn.commit()

            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="Parking lot not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"car_count": car, "message": "Detection and update successful"}

# 아래부터 클라이언트 통신
@app.get("/ParkingLots/", response_model=List[Lot])
async def read_lots():
    with engine.connect() as conn:
        result = conn.execute(select(parkinglots))
        parking_list = result.fetchall()
        return [Lot(id=row[0], name=row[1], image=row[2], cnt = row[3]) for row in parking_list]


@app.get("/ParkingLots/{lot_id}", response_model=Lot)
async def read_lot(lot_id: int):
    with engine.connect() as conn:
        result = conn.execute(select(parkinglots).where(parkinglots.c.id == lot_id))
        lot = result.fetchall()
        if lot:
            return lot
        else:
            raise HTTPException(status_code=404, detail="User not found")

@app.post("/ParkingLots/", response_model=Lots)
async def create_lot(new_name: str):
    with engine.connect() as conn:
        result = conn.execute(insert(parkinglots).values(name = new_name))
        conn.commit()
        new_user_id = result.lastrowid
        return Lots(id=new_user_id, name=new_name) 