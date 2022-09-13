import dxcam
import torch
import cv2
import numpy as np
import time
import math
import keyboard
import threading
import serial
import tkinter as tk
import pywintypes
import win32api
import win32con



def cooldown(cooldown_bool,wait):
    time.sleep(wait)
    cooldown_bool[0] = True


def labels():
    #This function contains all the labels used and is threaded so tikinter can run a ui 
    global fps_label
    global trigger_label
    global assist_label
    global silent_label
    global fov_label
    fps_label = tk.Label(text = "  ", font=('Tahoma','10'), fg='white', bg='black')
    fps_label.master.overrideredirect(True)
    fps_label.master.geometry("+14+16")
    fps_label.master.lift()
    fps_label.master.wm_attributes("-topmost", True)
    fps_label.master.wm_attributes("-disabled", True)
    fps_label.master.wm_attributes("-transparentcolor", "black")
    fps_label.pack()
    fov_label = tk.Label(text = f"FOV: {activation_range}", font=('Tahoma','10'), fg='white', bg='black')
    fov_label.master.overrideredirect(True)
    fov_label.master.lift()
    fov_label.master.wm_attributes("-topmost", True)
    fov_label.master.wm_attributes("-disabled", True)
    fov_label.master.wm_attributes("-transparentcolor", "black")
    fov_label.pack()
    trigger_label = tk.Label(text = "Triggerbot: Unactive", font=('Tahoma','10'), fg='red', bg='black')
    trigger_label.master.overrideredirect(True)
    trigger_label.master.lift()
    trigger_label.master.wm_attributes("-topmost", True)
    trigger_label.master.wm_attributes("-disabled", True)
    trigger_label.master.wm_attributes("-transparentcolor", "black")
    trigger_label.pack()
    assist_label = tk.Label(text = "Aim Assist: Unactive", font=('Tahoma','10'), fg='red', bg='black')
    assist_label.master.overrideredirect(True)
    assist_label.master.lift()
    assist_label.master.wm_attributes("-topmost", True)
    assist_label.master.wm_attributes("-disabled", True)
    assist_label.master.wm_attributes("-transparentcolor", "black")
    assist_label.pack()
    silent_label = tk.Label(text = "Silent aim: Unactive", font=('Tahoma','10'), fg='red', bg='black')
    silent_label.master.overrideredirect(True)
    silent_label.master.lift()
    silent_label.master.wm_attributes("-topmost", True)
    silent_label.master.wm_attributes("-disabled", True)
    silent_label.master.wm_attributes("-transparentcolor", "black")
    silent_label.pack()


    hWindow = pywintypes.HANDLE(int(fps_label.master.frame(), 16))
    exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
    win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)
    hWindow = pywintypes.HANDLE(int(assist_label.master.frame(), 16))
    exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
    win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)
    hWindow = pywintypes.HANDLE(int(trigger_label.master.frame(), 16))
    exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
    win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)
    fps_label.mainloop()



SENS = 0.313
AIM_SPEED = 1*(1/SENS)
target_multiply = [0,1.01,1.025,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05]
serialcomm = serial.Serial("COM3",115200,timeout = 0)
activation_range = 100

ui = threading.Thread(target=labels, args=())
ui.start()

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
model = torch.hub.load(r'C:\Users\PyPit\OneDrive\Desktop\cheats\yolov5' , 'custom', path= r'C:\Users\PyPit\OneDrive\Desktop\cheats\half.engine',source='local').cpu()
model.conf = 0.40
model.maxdet = 10
model.apm = True 
model.classes = [1]
camera = dxcam.create(output_idx=0, output_color="BGRA")

start_time = time.time()
x = 1
counter = 0






while True:
    closest_part_distance = 100000
    closest_part = -1
    screenshot = camera.grab(region)
    if screenshot is None: continue
    df = model(screenshot, size=736).pandas().xyxy[0]

    counter+= 1
    if(time.time() - start_time) > x:
        fps = "Fps:"+ str(int(counter/(time.time() - start_time)))
        fps_label.config(text=fps)
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
            if triggerbot:
                trigger_label.config(text = "Triggerbot: Active", fg= 'green')
            else:
                trigger_label.config(text = "Triggerbot: Unactive", fg= 'red')
            print(triggerbot)
            triggerbot_toggle[0] = False
            thread = threading.Thread(target=cooldown, args=(triggerbot_toggle,0.2,))
            thread.start()

    if keyboard.is_pressed('alt'):
        if aim_assist_toggle[0] == True:
            aim_assist = not aim_assist
            if aim_assist:
                assist_label.config(text = "Aim Assist: Active", fg= 'green')
            else:
                assist_label.config(text = "Aim Assist: Unactive", fg= 'red')
            print(aim_assist)
            aim_assist_toggle[0] = False
            thread = threading.Thread(target=cooldown, args=(aim_assist_toggle,0.2,))
            thread.start()
    
    if keyboard.is_pressed('p'):
        if silent_toggle[0] == True:
            silent_aim = not silent_aim
            if silent_aim:
                silent_label.config(text = "Silent Aim: Active", fg= 'green')
            else:
                silent_label.config(text = "Silent Aim: Unactive", fg= 'red')
            print(silent_aim)
            silent_toggle[0] = False
            thread = threading.Thread(target=cooldown, args=(silent_toggle,0.2,))
            thread.start()

    elif keyboard.is_pressed('up') and no_fov_cooldown[0] == True:
        activation_range += 5
        fov_label.config(text=f"FOV: {activation_range}")
        no_fov_cooldown[0] = False
        thread = threading.Thread(target=cooldown, args=(no_fov_cooldown,0.05,))
        thread.start()

    elif keyboard.is_pressed('down') and no_fov_cooldown[0] == True:
        activation_range -= 5
        fov_label.config(text=f"FOV: {activation_range}")
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
            thread = threading.Thread(target=cooldown, args=(send_next,0.06,))
            thread.start()




a
    # cv2.imshow("frame",screenshot)
    # if(cv2.waitKey(1) == ord('l')):
    #     cv2.destroyAllWindows()
    #     break