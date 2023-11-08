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
# model2 = models.get("yolo_nas_m", pretrained_weights ="coco").to(device)
# model3 = models.get("yolo_nas_s", pretrained_weights ="coco").to(device)

test_imgs = ["Test_video/test_photo1.jpg", "Test_video/test_photo2.jpg", "Test_video/test_photo3.jpg", "Test_video/test_photo4.jpg"]

for img in test_imgs:
    now = cv2.imread(img)
    now = cv2.cvtColor(now, cv2.COLOR_BGR2RGB)
    now = cv2.resize(now, (0, 0), fx=0.5, fy=0.5)


    results = model1.predict(now, conf=0.25, fuse_model= False)

    for result in results :
        labels = result.prediction.labels

    labels = list(labels)
    cnt = labels.count(2) + labels.count(7)

    print("인식된 차량의 개수: " + str(cnt))
