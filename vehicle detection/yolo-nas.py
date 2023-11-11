import cv2
import torch
from super_gradients.training import models

#-- GPU 설정
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)
use_cuda = torch.cuda.is_available()
print(use_cuda)
if use_cuda:
  print(torch.cuda.get_device_name(0))

#-- 사전학습된 Yolo_nas_small 모델 불러오기(빠르지만 정확도가 낮음)
model1 = models.get("yolo_nas_l", pretrained_weights ="coco").to(device)

def count_car(img):
    img = cv2.imread(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
 

    results = model1.predict(img, conf=0.25, fuse_model= False)

    for result in results :
        labels = result.prediction.labels

    labels = list(labels)

    count_car = 0
    count_truck = 0
    for num in labels:
        if num == 2:
            count_car += 1
        elif num == 7:
            count_truck += 1
    cnt = count_car + count_truck
    # print("인식된 차량의 개수: " + str(cnt))

    return(cnt)