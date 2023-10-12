import streamlit as st
import cv2
import numpy as np
import time


session_state = st.session_state


if 'reservations_counter' not in session_state:
    session_state.reservations_counter = 0
if 'releases_counter' not in session_state:
    session_state.releases_counter = 0


yolo_cfg = 'yolov3.cfg'
yolo_weights = 'yolov3.weights'


yolo_classes = 'coco.names'


with open(yolo_classes, 'r') as f:
    classes = f.read().strip().split('\n')

 
net = cv2.dnn.readNet(yolo_weights, yolo_cfg)


video_capture = cv2.VideoCapture('test2.mp4')  


total_parking_spots = 50  # 


parking_spot_status = [False] * total_parking_spots  
reservation_status = [None] * total_parking_spots  


def reserve_parking_spot(spot_number, user_id):
    if not parking_spot_status[spot_number]:
        parking_spot_status[spot_number] = True
        reservation_status[spot_number] = {
            "user_id": user_id,
            "start_time": time.time()
        }
        return True
    else:
        return False


def release_parking_spot(spot_number):
    if parking_spot_status[spot_number]:
        parking_spot_status[spot_number] = False
        end_time = time.time()
        start_time = reservation_status[spot_number]["start_time"]
        
        reservation_status[spot_number] = None
        return True
    else:
        return False


st.title('Car Detection and Parking Reservation')


video_display = st.image([], channels='BGR')

reserve_button = st.button('Reserve Parking Spot')
release_button = st.button('Release Parking Spot')


st.sidebar.header('Parking Information')
st.sidebar.write(f'Reservations: {session_state.reservations_counter}')
st.sidebar.write(f'Releases: {session_state.releases_counter}')
st.sidebar.write(f'Total Parking Spots: {total_parking_spots}')

while True:
    ret, frame = video_capture.read()

    
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)

    
    net.setInput(blob)

    layer_names = net.getUnconnectedOutLayersNames()
    outs = net.forward(layer_names)

    
    class_ids = []
    confidences = []
    boxes = []

    
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:  
                center_x = int(detection[0] * frame.shape[1])
                center_y = int(detection[1] * frame.shape[0])
                width = int(detection[2] * frame.shape[1])
                height = int(detection[3] * frame.shape[0])

               
                x = int(center_x - width / 2)
                y = int(center_y - height / 2)

                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, width, height])

 
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    
    car_count = len(indices)


    available_parking_spots = total_parking_spots - car_count


    if reserve_button:
        
        for spot_number in range(total_parking_spots):
            if not parking_spot_status[spot_number]:
                user_id = "Lee"
                if reserve_parking_spot(spot_number, user_id):
                    st.write(f"Reserved parking spot {spot_number} for user {user_id}")
                    cv2.putText(frame, f'reservation: {spot_number}', (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    session_state.reservations_counter += 1 
                    break
                else:
                    st.write(f"Parking spot {spot_number} is already taken")

    elif release_button:
      
        user_id = "user123"  
        spot_number = 0  
        if release_parking_spot(spot_number):
            st.write(f"Released parking spot {spot_number} for user {user_id}")
            session_state.releases_counter += 1  # Increment the releases counter by 1
        else:
            st.write(f"Parking spot {spot_number} is already vacant")

    if len(indices) > 0:
        for i in indices.flatten():
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = confidences[i]

            
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
            text = f'{label}: {confidence:.2f}'
            cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)

 
    cv2.putText(frame, f'Car Count: {car_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(frame, f'Available Parking Spots: {available_parking_spots}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

  
    
    video_display.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), width=800)


    st.markdown(
        """
        <style>
        .stButton > button {
            background-color: #008CBA;
            color: white;
            font-weight: bold;
            border: 2px solid #005687;
        }
        .stButton > button:hover {
            background-color: #005687;
        }
        .stSidebar {
            background-color: #f0f6f6;
            padding: 10px;
            border-radius: 5px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
