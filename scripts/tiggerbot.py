from typing import Counter
from mss import mss
import torch
import cv2
import numpy as np
import time
import math
import keyboard
import threading


def cooldown(cooldown_bool,wait):
    time.sleep(wait)
    cooldown_bool[0] = True

MONITOR_WIDTH = 1920#game res
MONITOR_HEIGHT = 1080#game res
MONITOR_SCALE = 5#how much the screen shot is downsized by eg. 5 would be one fifth of the monitor dimensions
region = (int(MONITOR_WIDTH/2-MONITOR_WIDTH/MONITOR_SCALE/2),int(MONITOR_HEIGHT/2-MONITOR_HEIGHT/MONITOR_SCALE/2),int(MONITOR_WIDTH/2+MONITOR_WIDTH/MONITOR_SCALE/2),int(MONITOR_HEIGHT/2+MONITOR_HEIGHT/MONITOR_SCALE/2))
x,y,width,height = region
screenshot_center = [int((width-x)/2),int((height-y)/2)]
triggerbot = False
triggerbot_toggle = [True]
model = torch.hub.load(r'C:\Users\PyPit\OneDrive\Desktop\cheats\yolov5' , 'custom', path= r'C:\Users\PyPit\OneDrive\Desktop\cheats\half.engine',source='local')
model.conf = 0.40
model.maxdet = 10
model.apm = True 
model.classes = [1]


start_time = time.time()
x = 1
counter = 0





with mss() as stc:
    while True:
        closest_part_distance = 100000
        closest_part = -1
        screenshot = np.array(stc.grab(region))
        df = model(screenshot, size=736).pandas().xyxy[0]

        counter+= 1
        if(time.time() - start_time) > x:
            fps = "fps:"+ str(int(counter/(time.time() - start_time)))
            print(fps)
            counter = 0
            start_time = time.time()



        for i in range(0,10):
            try:
                xmin = int(df.iloc[i,0])
                ymin = int(df.iloc[i,1])
                xmax = int(df.iloc[i,2])
                ymax = int(df.iloc[i,3])

                centerX = (xmax-xmin)/2+xmin 
                centerY = (ymax-ymin)/2+ymin

                distance = math.dist([centerX,centerY],screenshot_center)

                if int(distance) < closest_part_distance:
                    closest_part_distance = distance
                    closest_part = i

                # cv2.rectangle(screenshot,(xmin,ymin),(xmax,ymax), (255,0,0),3)
            except:
                print("",end="")


        if keyboard.is_pressed('`'):
            if triggerbot_toggle[0] == True:
                triggerbot = not triggerbot
                print(triggerbot)
                triggerbot_toggle[0] = False
                thread = threading.Thread(target=cooldown, args=(triggerbot_toggle,0.2,))
                thread.start()

        if closest_part != -1:
            xmin = df.iloc[closest_part,0]
            ymin = df.iloc[closest_part,1]
            xmax = df.iloc[closest_part,2]
            ymax = df.iloc[closest_part,3]
            if triggerbot == True and screenshot_center[0] in range(int(xmin),int(xmax)) and screenshot_center[1] in range(int(ymin),int(ymax)):
                keyboard.press_and_release("k")
                




        # cv2.imshow("frame",screenshot)
        # if(cv2.waitKey(1) == ord('l')):
        #     cv2.destroyAllWindows()
        #     break