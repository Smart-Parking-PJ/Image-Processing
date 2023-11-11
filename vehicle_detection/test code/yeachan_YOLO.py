import cv2
import numpy as np

# YOLO 모델 파일과 클래스 파일을 다운로드한 경로로 수정하세요.
model_weights = 'vehicle detection\YOLO model\yolov3.weights'
model_config = 'vehicle detection\YOLO model\yolov3.cfg'
class_file = 'vehicle detection\YOLO model\coco.names'

# 클래스 이름을 로드합니다.
classes = []
with open(class_file, 'r') as f:
    classes = f.read().strip().split('\n')

# YOLO 모델을 로드합니다.
net = cv2.dnn.readNet(model_weights, model_config)

# 비디오 파일을 열거나 웹캠을 사용하려면 VideoCapture 객체를 생성합니다.
# 비디오 파일을 사용하려면 파일 경로를, 웹캠을 사용하려면 카메라 장치 번호를 입력하세요.
cap = cv2.VideoCapture('Test_video/school1.mp4')  # 비디오 파일 경로를 수정하세요.
# cap = cv2.VideoCapture(0)  # 웹캠 사용 예시

while True:
    cnt = 0
    ret, frame = cap.read()

    if not ret:
        break

    height, width, _ = frame.shape

    # YOLO 입력 이미지 준비
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(net.getUnconnectedOutLayersNames())

    # 검출된 객체 정보를 저장할 리스트
    class_ids = []
    confidences = []
    boxes = []

    # 객체를 검출하고 정보 저장
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and classes[class_id] == 'car':
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # 객체의 사각형 좌표 계산
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # NMS (Non-maximum suppression)를 사용하여 중복된 객체 제거
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = confidences[i]

            # 검출된 객체 주위에 사각형 그리기
            color = (0, 255, 0)  # 객체 유형에 따라 색상을 변경할 수 있습니다.
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            cnt += 1
    print("차량의 수: ", cnt)

    cv2.imshow("Car Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
