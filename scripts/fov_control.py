from mss import mss
import torch
import cv2
import numpy as np
import time
import math
import keyboard
import threading
import serial

def cooldown(cooldown_bool,wait):
    time.sleep(wait)
    cooldown_bool[0] = True


SENS = 0.313
AIM_SPEED = 1*(1/SENS)
target_multiply = [0,1.01,1.025,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05]
serialcomm = serial.Serial("COM3",115200,timeout = 0)
activation_range = 100


MONITOR_WIDTH = 1920#game res
MONITOR_HEIGHT = 1080#game res
MONITOR_SCALE = 5#how much the screen shot is downsized by eg. 5 would be one fifth of the monitor dimensions
region = (int(MONITOR_WIDTH/2-MONITOR_WIDTH/MONITOR_SCALE/2),int(MONITOR_HEIGHT/2-MONITOR_HEIGHT/MONITOR_SCALE/2),int(MONITOR_WIDTH/2+MONITOR_WIDTH/MONITOR_SCALE/2),int(MONITOR_HEIGHT/2+MONITOR_HEIGHT/MONITOR_SCALE/2))
x,y,width,height = region
screenshot_center = [int((width-x)/2),int((height-y)/2)]
triggerbot = False
triggerbot_toggle = [True]
aim_assist = False
aim_assist_toggle = [True]
send_next = [True]
silent_aim = False
silent_aim_not_cooldown = [True]
silent_toggle = [True]
no_fov_cooldown = [True]
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

        if keyboard.is_pressed('alt'):
            if aim_assist_toggle[0] == True:
                aim_assist = not aim_assist
                print(aim_assist)
                aim_assist_toggle[0] = False
                thread = threading.Thread(target=cooldown, args=(aim_assist_toggle,0.2,))
                thread.start()
        
        if keyboard.is_pressed('p'):
            if silent_toggle[0] == True:
                silent_aim = not silent_aim
                print(silent_aim)
                silent_toggle[0] = False
                thread = threading.Thread(target=cooldown, args=(silent_toggle,0.2,))
                thread.start()

        elif keyboard.is_pressed('up') and no_fov_cooldown[0] == True:
            activation_range += 5
            no_fov_cooldown[0] = False
            thread = threading.Thread(target=cooldown, args=(no_fov_cooldown,0.05,))
            thread.start()

        elif keyboard.is_pressed('down') and no_fov_cooldown[0] == True:
            activation_range -= 5
            no_fov_cooldown[0] = False
            thread = threading.Thread(target=cooldown, args=(no_fov_cooldown,0.05,))
            thread.start()

        if closest_part != -1:
            xmin = df.iloc[closest_part,0]
            ymin = df.iloc[closest_part,1]
            xmax = df.iloc[closest_part,2]
            ymax = df.iloc[closest_part,3]

            head_center_list = [(xmax-xmin)/2+xmin,(ymax-ymin)/2+ymin]
            if triggerbot == True and screenshot_center[0] in range(int(xmin),int(xmax)) and screenshot_center[1] in range(int(ymin),int(ymax)):
                serialcomm.write("shoot".encode())

            if silent_aim == True and silent_aim_not_cooldown[0] == True:
                xdif = (head_center_list[0]-screenshot_center[0])*AIM_SPEED*target_multiply[MONITOR_SCALE]
                ydif = (head_center_list[1]-screenshot_center[1])*AIM_SPEED*target_multiply[MONITOR_SCALE]
                data = f"silent{int(xdif)}:{int(ydif)}"
                serialcomm.write(data.encode())
                silent_aim_not_cooldown[0] = False
                thread = threading.Thread(target=cooldown, args=(silent_aim_not_cooldown,0.2,))
                thread.start()

            if aim_assist == True and closest_part_distance < activation_range and send_next[0] == True:
                xdif = (head_center_list[0] - screenshot_center[0])*AIM_SPEED*target_multiply[MONITOR_SCALE]
                ydif = (head_center_list[1] - screenshot_center[1])*AIM_SPEED*target_multiply[MONITOR_SCALE]
                data = f"{int(xdif)}:{int(ydif)}"
                serialcomm.write(data.encode())
                send_next[0] = False
                thread = threading.Thread(target=cooldown, args=(send_next,0.05,))
                thread.start()





        # cv2.imshow("frame",screenshot)
        # if(cv2.waitKey(1) == ord('l')):
        #     cv2.destroyAllWindows()
        #     break