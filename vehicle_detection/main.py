import cv2
from get_frame import frame_get


video_path="vehicle_detection/Test_video/1.mp4"
cap = cv2.VideoCapture(video_path)

frame_get(cap)