import cv2

# Haar Cascade 분류기를 불러옵니다.
car_cascade = cv2.CascadeClassifier('vehicle detection\model\haarcascade_car.xml') # 모델 파일 경로를 수정하세요.

# 비디오 파일을 열거나 웹캠을 사용하려면 VideoCapture 객체를 생성합니다.
# 비디오 파일을 사용하려면 파일 경로를, 웹캠을 사용하려면 카메라 장치 번호를 입력하세요.
cap = cv2.VideoCapture('Test_video/test2.mp4')  # 비디오 파일 경로를 수정하세요.
# cap = cv2.VideoCapture(0)  # 웹캠 사용 예시

while True:
    # 프레임 읽기
    ret, frame = cap.read()

    if not ret:
        break

    # 그레이스케일로 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 자동차 검출 수행
    cars = car_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # 검출된 자동차 주위에 사각형 그리기
    for (x, y, w, h) in cars:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # 결과를 화면에 표시
    cv2.imshow('Car Detection', frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 비디오 캡처 객체와 창 닫기
cap.release()
cv2.destroyAllWindows()
