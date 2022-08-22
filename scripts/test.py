
import dxcam
import numpy as np
from mss import mss
import cv2
import time
import sys


cam = dxcam.create(device_idx=0, output_idx=0, output_color= "BGRA")
# sleep(3)
MONITOR_WIDTH = 1920#base res
MONITOR_HEIGHT = 1080#base res
MONITOR_SCALE = 5#how much the screen shot is downsized by eg. 5 would be one fifth of the monitor dimensions


region = (int(MONITOR_WIDTH/2-MONITOR_WIDTH/MONITOR_SCALE/2),int(MONITOR_HEIGHT/2-MONITOR_HEIGHT/MONITOR_SCALE/2),int(MONITOR_WIDTH/2+MONITOR_WIDTH/MONITOR_SCALE/2),int(MONITOR_HEIGHT/2+MONITOR_HEIGHT/MONITOR_SCALE/2))
x = 1
counter = 0
start_time = time.time()

with mss() as stc:
    while True:
        # np.set_printoptions(threshold=sys.maxsize)
        # np.set_printoptions(linewidth=np.inf)
        img = (stc.grab(region))
        
        if img is None: continue

        
        counter+=1
        if (time.time() - start_time) > x :
            fps = "FPS: "+str(int(counter / (time.time() - start_time)))
            print(fps)
            counter = 0
            start_time = time.time()
        # print((img.all()))
        # print(img)
        # sleep(1)
        # cv2.imshow("frame", img)
        # if(cv2.waitKey(1) == ord('q')):
        #     cv2.destroyAllWindows()
        


