import cv2
import numpy as np
from time import sleep

largura_min = 80  # 차량을 감지하기 위한 최소 폭
altura_min = 80   # 차량을 감지하기 위한 최소 높이

offset = 6  # 픽셀 간 허용 오차  

pos_linha = 550  # 차량을 세기 위한 행 위치 

delay = 60  # 비디오의 초당 프레임 수

detec = []  # 감지된 차량의 중심 좌표를 저장할 리스트
carros = 0  # 감지된 차량 수

def pega_centro(x, y, w, h):
    # 객체의 경계 상자의 중심 좌표를 계산하여 반환
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx, cy

# 비디오 캡처 객체 생성 및 설정
try:
    cap = cv2.VideoCapture('Test_video\KakaoTalk_20231010_181752927.mp4')
    if not cap.isOpened():
        raise Exception("비디오 파일 열기 실패.")

    # 배경 제거 모델 초기화
    subtracao = cv2.bgsegm.createBackgroundSubtractorMOG()

    while True:
        ret, frame1 = cap.read()
        if not ret:
            break
        # 비디오가 너무 빠르게 처리되지 않도록 설정
        tempo = float(1 / delay)
        sleep(tempo) 
        
        # 프레임을 그레이스케일로 변환하고 블러 처리
        grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(grey, (3, 3), 5)
        
        # 배경 제거 적용
        img_sub = subtracao.apply(blur)
        
        # 모폴로지 연산을 통해 이미지 세밀화
        dilat = cv2.dilate(img_sub, np.ones((5, 5)))
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        dilatada = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)
        dilatada = cv2.morphologyEx(dilatada, cv2.MORPH_CLOSE, kernel)
        
        # 객체 감지를 위해 경계 상자 찾기
        contorno, h = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # 카운팅 라인 그리기
        cv2.line(frame1, (25, pos_linha), (1200, pos_linha), (255, 127, 0), 3) 

        for (i, c) in enumerate(contorno):
            (x, y, w, h) = cv2.boundingRect(c)
            validar_contorno = (w >= largura_min) and (h >= altura_min)
            if not validar_contorno:
                continue
    
            # 객체 경계 상자 그리기
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)        

            # 객체의 중심 좌표 계산하고 저장
            centro = pega_centro(x, y, w, h)
            detec.append(centro)
            
            # 객체를 세기 위한 카운터 업데이트
            for (x, y) in detec:
                if y < (pos_linha + offset) and y > (pos_linha - offset):
                    carros += 1
                    detec.remove((x, y))
                    print("차량이 감지되었습니다: " + str(carros))        
       
        # 화면에 차량 수 표시
        cv2.putText(frame1, "차량 수 : " + str(carros), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
        
        # 비디오 프레임 및 감지된 객체 표시
        cv2.imshow("비디오 원본", frame1)
        cv2.imshow("감지 결과", dilatada)

        if cv2.waitKey(1) == 27:
            break
except Exception as e:
    print("오류 발생:", str(e))
finally:
    cv2.destroyAllWindows()
    if 'cap' in locals():
        cap.release()
