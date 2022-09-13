from typing import Counter
from mss import mss
import torch
import cv2
import numpy as np
import time



MONITOR_WIDTH = 1920#game res
MONITOR_HEIGHT = 1080#game res
MONITOR_SCALE = 5#how much the screen shot is downsized by eg. 5 would be one fifth of the monitor dimensions
region = (int(MONITOR_WIDTH/2-MONITOR_WIDTH/MONITOR_SCALE/2),int(MONITOR_HEIGHT/2-MONITOR_HEIGHT/MONITOR_SCALE/2),int(MONITOR_WIDTH/2+MONITOR_WIDTH/MONITOR_SCALE/2),int(MONITOR_HEIGHT/2+MONITOR_HEIGHT/MONITOR_SCALE/2))


model = torch.hub.load(r'C:\Users\PyPit\OneDrive\Desktop\cheats\yolov5' , 'custom', path= r'C:\Users\PyPit\OneDrive\Desktop\cheats\best.pt',source='local')
model.conf = 0.40
model.maxdet = 10
model.apm = True 



start_time = time.time()
x = 1
counter = 0





with mss() as stc:
    while True:
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

                cv2.rectangle(screenshot,(xmin,ymin),(xmax,ymax), (255,0,0),3)
            except:
                print("",end="")

        cv2.imshow("frame",screenshot)
        if(cv2.waitKey(1) == ord('l')):
            cv2.destroyAllWindows()
            break