import cv2
import numpy as np
import time

count=0

# YOLO 로드
net = cv2.dnn.readNet("vehicle detection\YOLO model\yolov3.weights", "vehicle detection\YOLO model\yolov3.cfg")
classes = []
with open('vehicle detection\YOLO model\coco.names', "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i-1] for i in net.getUnconnectedOutLayers()]

# 영상 가져오기
video_path = "Test_video/KakaoTalk_20231010_181752927.mp4"  # 영상 파일 경로
cap = cv2.VideoCapture(0)

output_interval=10
last_output_time=time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    height, width, channels = frame.shape  # 프레임 속성 가져오기

    # 물체 감지
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # 정보 화면에 표시
    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            # 차량 및 트럭일 경우에만 처리
            if confidence > 0.5:
                if classes[class_id] == "car" or classes[class_id] == "truck":
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

    # 노이즈 제거
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    count=0
    # 최종
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            count=count+1
            confidence=confidences[i]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0,0,255), 2)
                
    print(f"현재 차량 수 : {count}")


            
        
    # 영상 프레임 출력
    cv2.imshow("video", frame)


    if cv2.waitKey(2) & 0xFF == ord('a'):
        break

# 영상 처리가 끝나면 영상을 닫습니다.
cap.release()
cv2.destroyAllWindows()
