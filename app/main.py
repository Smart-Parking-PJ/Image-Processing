from fastapi import FastAPI, UploadFile
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import IO

from app.api_communication import api_patch
from app.yolo_nas import YOLO


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()
yolo = YOLO()


@app.post("/photo/{idx}")
async def detection(file: UploadFile, idx: int):
    path = await save_file(file.file)
    car = await yolo.count_car(path)
    print("차량 개수= " + str(car))
    print("index: ", idx)
    await api_patch(idx, car, file)
    return car

async def save_file(file: IO):
    # s3 업로드라고 생각해 봅시다. delete=True(기본값)이면
    # 현재 함수가 닫히고 파일도 지워집니다.
    with NamedTemporaryFile("wb", delete=False) as tempfile:
        tempfile.write(file.read())
        return tempfile.name