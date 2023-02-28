import math
import cv2
import time
import numpy as np
import Hand_Tracking_Module as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc









# get the brightness
brightness = sbc.get_brightness()
# get the brightness for the primary monitor


# # set the brightness to 100%
# # sbc.set_brightness(100)
# # set the brightness to 100% for the primary monitor
# current_brig = sbc.get_brightness(100)
# primary_brig = sbc.get_brightness(display=0)
# brig_range =  (current_brig, primary_brig)
# sbc.set_brightness(0, None)
# min_brig = brig_range[0]
# max_brig = brig_range[1]
# brig = 0
# brig_bar = 400
# brig_perc = 0





devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
vol_range = volume.GetVolumeRange()

min_vol = vol_range[0]
max_vol = vol_range[1]
vol = 0
vol_bar = 400
vol_perc = 0




ip = "192.168.176.36"
cap = cv2.VideoCapture(f"http://{ip}:4747/video?1200x720")

# wid_cam, hei_cam = 1200, 720
# cap.set(3, wid_cam)
# cap.set(4, hei_cam)
 

# prev_time = 0
# pres_time = 0


detector = htm.hand_detector(detectionCon=0.7)


while True:
    success, img = cap.read()
    img = detector.find_hands(img)
    lm_list = detector.find_position_of_hands(img, draw = False)
    
    if len(lm_list) != 0:
        # print(lm_list[4], lm_list[8])
        x1, y1 = lm_list[4][1], lm_list[4][2]
        x2, y2 = lm_list[8][1], lm_list[8][2]
        cx, cy = (x1 + x2)// 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
        # cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)
        if length < 50:
            cv2.circle(img, (cx, cy), 12, (0, 255, 0), cv2.FILLED)

        vol = np.interp(length, [50, 300], [min_vol, max_vol])
        vol_bar = np.interp(length, [50, 300], [400, 150])
        vol_perc = np.interp(length, [50, 300], [0, 100])
        volume.SetMasterVolumeLevel(vol, None)
        # print(int(length), vol)

        cv2.rectangle(img, (50, 150), (75, 400), (0, 255, 0), 3)
        cv2.rectangle(img, (50, int(vol_bar)), (75, 400), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, "Vol. Control", (20, 140), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 3)
        cv2.putText(img, f"{int(vol_perc)} %", (36, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)


        '''
        the brightness control section        
        '''

        # bx1, by1 = lm_list[4][1], lm_list[4][2]
        # bx2, by2 = lm_list[12][1], lm_list[12][2]
        # bcx, bcy = (bx1 + bx2)// 2, (by1 + by2) // 2

        # cv2.circle(img, (bx1, by1), 12, (255, 0, 255), cv2.FILLED)
        # cv2.circle(img, (bx2, by2), 12, (255, 0, 255), cv2.FILLED)
        # cv2.line(img, (bx1, by1), (bx2, by2), (0, 0, 255), 3)
        # cv2.circle(img, (bcx, bcy), 12, (255, 0, 255), cv2.FILLED)
        # brig_length = math.hypot(bx2 - bx1, by2 - by1)
        # if brig_length < 50:
        #     cv2.circle(img, (bcx, bcy), 12, (0, 255, 0), cv2.FILLED)

        # brig = np.interp(brig_length, [50, 300], [0, 100])
        # brig_bar = np.interp(brig_length, [50, 300], [400, 150])
        # brig_perc = np.interp(brig_length, [50, 300], [0, 100])
        # sbc.set_brightness(int(brig))

        # cv2.rectangle(img, (600, 150), (620, 400), (0, 255, 0), 3)
        # cv2.rectangle(img, (600, int(brig_bar)), (620, 400), (0, 255, 0), cv2.FILLED)
        # cv2.putText(img, "Brightness Control", (510, 140), cv2.FONT_HERSHEY_PLAIN, 0.9, (0, 255, 0), 3)
        # cv2.putText(img, f"{int(brig_perc)}%", (570, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)




    # adding  frame rate
    # pres_time = time.time()
    # fps = 1/(pres_time - prev_time)
    # prev_time = pres_time
    # cv2.putText(img, f"FPS: {int(fps)}", (40, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
    

    cv2.imshow("Volume Control", img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()