import time
import cv2

video_path="vehicle detection/Test_video/test2.mp4" #영상 주소
cap = cv2.VideoCapture(video_path)
last_output_time=time.time() 
output_time=2 #5 or 10

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    video_current_time=time.time() #현재 시간

    if(video_current_time-last_output_time>=output_time): #n초마다 영상 캡쳐
        cv2.imshow("video", frame)
        print("image save")
        last_output_time=video_current_time

    if cv2.waitKey(1) & 0xFF == ord('a'): #종료
        break

cap.release()
cv2.destroyAllWindows()
