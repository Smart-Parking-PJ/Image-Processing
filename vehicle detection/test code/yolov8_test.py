import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('vehicle detection\YOLO model\yolov8n.pt')

# 동영상 파일 사용시
video_path = "Test_video/test2.mp4"
cap = cv2.VideoCapture(video_path)

# webcam 사용시
# cap = cv2.VideoCapture(0)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        results = model(frame)
        cnt = 0
        for result in results:
            boxes = result.boxes.cpu().numpy()
            for i, box in enumerate(boxes):
                name = result.names[int(box.cls[0])]
                if name == "car" or name == "truck":
                    cnt += 1
                    r = box.xyxy[0].astype(int)
                    cv2.rectangle(frame, r[:2], r[2:], (255, 255, 255), 2)

        cv2.imshow("YOLOv8 Inference", frame)
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()