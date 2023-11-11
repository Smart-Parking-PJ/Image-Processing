import time
import cv2
import numpy as np
import os

video_path="Test_video/test2.mp4" #영상 주소
cap = cv2.VideoCapture(video_path)
last_output_time=time.time() 
output_time=2 #5 or 10
count=1;  
save_picture="vehicle detection/daeun/peacture" #파일 저장 주소
os.makedirs(save_picture, exist_ok=True)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    cv2.imshow("video", frame)
    video_current_time=time.time() #현재 시간

    if(video_current_time-last_output_time>=output_time): #n초마다 영상 캡쳐
        file_name = "time_picture%d.jpeg" %count  # 파일 이름 설정
        file_path=os.path.join(save_picture,file_name)
        cv2.imwrite(file_path, frame) #사진 저장
        print("image save")
        count=count+1
        last_output_time=video_current_time

    if cv2.waitKey(1) & 0xFF == ord('a'): #종료
        break

cap.release()
cv2.destroyAllWindows()
