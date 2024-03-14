from fastapi import FastAPI, UploadFile
from pathlib import Path
from app.api_communication import api_patch
from app.yolo_nas import YOLO

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()

@app.post("/photo")
async def detection(files: UploadFile, idx: int):
    yolo = YOLO()
    car = await yolo.count_car(files)
    print("차량 개수= " + car)
    # await api_patch(id, car, files)
