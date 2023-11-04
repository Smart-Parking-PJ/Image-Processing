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
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# 영상 가져오기
video_path = "Test_video/KakaoTalk_20231010_181752927.mp4"  # 영상 파일 경로
cap = cv2.VideoCapture(video_path)

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

            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                #if
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # 노이즈 제거
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # 최종
    font = cv2.FONT_HERSHEY_PLAIN  # 글꼴
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence=confidences[i]
            color = colors[i]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            
#현재 인식하는 차량 수 출력
    current_time = time.time()
    if current_time - last_output_time >= output_interval:
        for i in range(len(boxes)):
            if i in indexes:
                label = str(classes[class_ids[i]])
                if(label=="car"or"truck"):
                    count=count+1
        print(f"현재 차량 수 : {count}")
        count=0
        last_output_time = current_time
        
    # 영상 프레임 출력
    cv2.imshow("video", frame)


    if cv2.waitKey(2) & 0xFF == ord('a'):
        break

# 영상 처리가 끝나면 영상을 닫습니다.
cap.release()
cv2.destroyAllWindows()
