import torch
from super_gradients.training import models
import supervision as sv


class YOLO:
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(device)
    use_cuda = torch.cuda.is_available()
    print(use_cuda)
    if use_cuda:
        print(torch.cuda.get_device_name(0))

    #-- 사전학습된 Yolo_nas_small 모델 불러오기(빠르지만 정확도가 낮음)
    model1 = models.get("yolo_nas_l", pretrained_weights ="coco").to(device)
    confs = [0.25, 0.5, 0.25, 0.2]
    async def count_car(self, img, idx):
        results = self.model1.predict(img, conf=self.confs[idx], fuse_model= False)
        results.save(output_path="pred.jpg")
        detections = sv.Detections.from_yolo_nas(results)
        count_car, count_truck = 0, 0
        for num in detections.class_id:
            if num == 2:
                count_car += 1
            elif num == 7:
                count_truck += 1
        cnt = count_car + count_truck
        print("인식된 차량의 개수: " + str(cnt))
        return cnt

    
if __name__ == "__main__":
    test = YOLO()
    print(test.count_car("app/test_img/test2.jpg", 1))