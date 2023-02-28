import cv2
import mediapipe as mp
import time

ip = "192.168.176.36"
cap = cv2.VideoCapture(f"http://{ip}:4747/video?640x480")

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# to measure the FPS
prev_time = 0
pres_time = 0


while True:
    success, img = cap.read()
    img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    
    results = hands.process(img) #process the frame
#  checking for multiple hands detected or not 
    # print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            # to chck the id number of each hands
            for id, lm in enumerate(hand_landmark.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(id, cx, cy)
                # making the first id point of the hand bigger i.e id number 0
                # if id == 0:
                #     cv2.circle(img, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)


            mp_draw.draw_landmarks(img, hand_landmark, mp_hands.HAND_CONNECTIONS)

    
    # measuring FPS
    pres_time = time.time()
    fps = 1/(pres_time - prev_time)
    prev_time = pres_time
    cv2.putText(img, f"FPS: {str(int(fps))}", (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0 , 255), 3)





    cv2.imshow("Hand tracking", img)
    cv2.waitKey(1)