import cv2
import torch
from super_gradients.training import models
import random
import numpy as np
#-- GPU 설정
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)
use_cuda = torch.cuda.is_available()
print(use_cuda)
if use_cuda:
  print(torch.cuda.get_device_name(0))

#-- 사전학습된 Yolo_nas_small 모델 불러오기(빠르지만 정확도가 낮음)
model1 = models.get("yolo_nas_l", pretrained_weights ="coco").to(device)
# model2 = models.get("yolo_nas_m", pretrained_weights ="coco").to(device)
# model3 = models.get("yolo_nas_s", pretrained_weights ="coco").to(device)

img = cv2.imread("Test_video/test_photo1.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)

results = model1.predict(img, conf=0.25)

for result in results :
    labels = result.prediction.labels

labels = list(labels)
cnt = labels.count(2) + labels.count(7)

print("인식된 차량의 개수: " + str(cnt))
results.show(box_thickness=2, show_confidence=True)