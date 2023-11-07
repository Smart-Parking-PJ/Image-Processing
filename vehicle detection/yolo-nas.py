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

img = cv2.imread("Test_video/test_photo4.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)

result = model1.predict(img, conf=0.25)

first_frame = True
output = result[0]
bboxes = output.prediction.bboxes_xyxy
confs = output.prediction.confidence
labels = output.prediction.labels
class_names = output.class_names

print(bboxes)
print(confs)
print(labels)
print(class_names)

result.show()