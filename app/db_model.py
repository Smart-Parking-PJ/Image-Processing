from pydantic import BaseModel

# 주차장 데이터를 위한 Pydantic 모델
class Lots(BaseModel):
    id: int
    name: str
    cnt: int

class Lot(BaseModel):
    id: int
    name: str
    image: str
    cnt: int

class Post_User(BaseModel):
    id: int
    name: str
    cnt: int