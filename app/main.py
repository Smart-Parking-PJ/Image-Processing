from fastapi import FastAPI, UploadFile
from pathlib import Path
from fastapi.responses import FileResponse

from app.api_communication import api_patch
from app.yolo_nas import YOLO
from app.file_control import save_file

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()
yolo = YOLO()

@app.post("/photo/{idx}")
async def detection(file: UploadFile, idx: int):
    path = await save_file(file.file)
    car = await yolo.count_car(path)
    print("차량 개수= " + str(car))
    print("index: ", idx)
    # await api_patch(idx, car, file)
    return car
@app.get("/")
async def test():
    return FileResponse("predicted/pred_0.jpg")