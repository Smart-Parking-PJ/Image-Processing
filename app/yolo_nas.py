import torch
from super_gradients.training import models

class YOLO:
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(device)
    use_cuda = torch.cuda.is_available()
    print(use_cuda)
    if use_cuda:
        print(torch.cuda.get_device_name(0))

    #-- 사전학습된 Yolo_nas_small 모델 불러오기(빠르지만 정확도가 낮음)
    model1 = models.get("yolo_nas_l", pretrained_weights ="coco").to(device)

    async def count_car(self, img):
        results = self.model1.predict(img, conf=0.25, fuse_model= False)
        results.save(output_folder="predicted/")
        labels = results[0].prediction.labels
        count_car = 0
        count_truck = 0
        for num in labels:
            if num == 2:
                count_car += 1
            elif num == 7:
                count_truck += 1
        cnt = count_car + count_truck
        print("인식된 차량의 개수: " + str(cnt))

        return cnt

    
if __name__ == "__main__":
    test = YOLO()
    print(test.count_car("app/test_img/test2.jpg"))