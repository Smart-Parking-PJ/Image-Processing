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
    api_patch(idx, car)
    return car