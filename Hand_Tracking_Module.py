"""
Creating a module of hand-tracker so as gto not write the same code again

"""

import cv2
import mediapipe as mp
import time



class hand_detector():
    # initializing
    def __init__(self, mode=False, maxHands = 2, complexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.complexity = complexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.maxHands, self.complexity, self.detectionCon, self.trackCon)
        self.mp_draw = mp.solutions.drawing_utils
    

    def find_hands(self, img, draw=True):
        img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_RGB) #process the frame
        #  checking for multiple hands detected or not 
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for hand_landmark in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, hand_landmark, self.mp_hands.HAND_CONNECTIONS)

        return img
                
                


    def find_position_of_hands(self, img, hand_num=0, draw = True):
        self.lm_list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_num]
            for id, lm in enumerate(my_hand.landmark):
                    # print(id, lm)
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    # print(id, cx, cy)
                    self.lm_list.append([id, cx, cy])
                    
                    # making the first id point of the hand bigger i.e id number 0
                    # if id == 0:
                    #     cv2.circle(img, (cx, cy), 1, (255, 0, 255))
                    # cv2.circle(img, (cx, cy), 1, (255, 20, 0), cv2.FILLED)
                    
        return self.lm_list


def main():  
    # to measure the FPS
    prev_time = 0
    pres_time = 0

    
    """ 
    use this method in a situatiion where the camera is blurry, 
    download droidcam on phone to use phone camera instead of the pc webcam 
    connect wirelessly with the ip address of the droid cam
    """
    ip = "192.168.176.36"
    cap = cv2.VideoCapture(f"http://{ip}:4747/video?640x480")
    # cap = cv2.VideoCapture(1)

    detector = hand_detector()

    while True:
        success, img = cap.read()
        img = detector.find_hands(img)
        lm_list = detector.find_position_of_hands(img)
        if len(lm_list) != 0:
            print(lm_list[4])

         # measuring FPS
        pres_time = time.time()
        fps = 1/(pres_time - prev_time)
        prev_time = pres_time
        cv2.putText(img, f"FPS: {str(int(fps))}", (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0 , 255), 3)


        
        cv2.imshow("Hand tracking", img)
        cv2.waitKey(1)




if __name__ == "__main__":
    main()