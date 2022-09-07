import dxcam
import torch
import cv2
import numpy as np
from mss import mss
import win32api
import win32con
import math
import keyboard
import time
import threading
import tkinter as tk
import pywintypes
import serial

SENS = 0.313
AIM_SPEED = 1*(1/SENS)#aim speed/sens for aimbot
activation_range = 20#activation range for aim assist
serialcomm = serial.Serial('COM3',115200, timeout = 0)#com port for arduino
MONITOR_WIDTH = 1920#base res
MONITOR_HEIGHT = 1080#base res
MONITOR_SCALE = 1.3#how much the screen shot is downsized by eg. 5 would be one fifth of the monitor dimensions




def cooldown(cooldown_bool,wait):
    #cooldown threed for toggels or cooldowns
    time.sleep(wait)
    cooldown_bool[0] = True

def shoot():
    #Sends Arduino message to fire
    data = "shoot"
    serialcomm.write(data.encode())
    # print(data)

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

    



if __name__ == "__main__":
    #creating fps overlay for the program
    ui = threading.Thread(target=labels, args=())
    ui.start()



    """
    Main part  of the program
    """
    target_multiply= [0,1.01,1.025,1.05,1.05,1.05,1.05,1.05,1.05,1.05] #depending on the screen ratio how much you move the mouse
    no_fov_cooldown = [True]
    triggerbot = False
    triggerbot_toggle = [True]
    silent_aim = False
    silent_aim_not_cooldown = [True]
    silent_aim_toggle = [True]
    aim_assist = False
    send_next = [True]
    aim_assist_toggle = [True]
    model = torch.hub.load(r'C:\Users\PyPit\OneDrive\Documents\CODE\Valorant_arduino\yolov5', 'custom', path=r"C:\Users\PyPit\OneDrive\Documents\CODE\Valorant_arduino\scripts\best_nano.engine", _verbose=False, source= "local").eval().cuda()#loading model onto gpu
    model.conf = 0.25# model confidance threshold
    # model.iou = 0.45# overlap threshhold threshold
    model.classes  = [0,1] # which classe the model detects
    model.maxdet = 30# max detections
    model.amp = True# amps model 
    camera = dxcam.create(device_idx=0, output_idx=0, output_color= "BGRA") #making the dxcam 
    region = (int(MONITOR_WIDTH/2-MONITOR_WIDTH/MONITOR_SCALE/2),int(MONITOR_HEIGHT/2-MONITOR_HEIGHT/MONITOR_SCALE/2),int(MONITOR_WIDTH/2+MONITOR_WIDTH/MONITOR_SCALE/2),int(MONITOR_HEIGHT/2+MONITOR_HEIGHT/MONITOR_SCALE/2))
    x,y,width,height = region
    screenshot_center = [int((width-x)/2),int((height-y)/2)]
    

    print(region)
    start_time = time.time()
    x = 1
    counter = 0
    # (int(monitor_width/2-monitor_width/monitor_scale/2),int(monitor_height/2-monitor_height/monitor_height/2),int(monitor_width/2+monitor_width/monitor_scale/2),int(monitor_height/2+monitor_height/monitor_height/2))
    # (768, 432, 1152, 648)
    # {"top": 350, "left": 640, "width": 640, "height":400}

    while True:
        
        screenshot = camera.grab(region)
        if screenshot is None: continue
        counter+=1
        if (time.time() - start_time) > x :
            fps = "FPS: "+str(int(counter / (time.time() - start_time)))
            fps_label.config(text=fps)
            counter = 0
            start_time = time.time()
        df= model(screenshot, size=640).pandas().xyxy[0]
        closest_part_distance = 1000000
        closest_part =-1


        for i in range(0,30):
            try:

                xmin = int(df.iloc[i,0])
                ymin = int(df.iloc[i,1])
                xmax = int(df.iloc[i,2])
                ymax = int(df.iloc[i,3])


                # cv2.putText(screenshot,str(int(float(df.iloc[i,4])*100)), (xmin, ymin), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),1,1)
                if int(df.iloc[i,5]) == 0:
                    cv2.rectangle(screenshot, (xmin, ymin), (xmax, ymax),(0,0,255) , 2)
                    head_center_list = [int((xmax-xmin)/2+xmin),int((ymax-ymin)/2+ymin)]
                    cv2.line(screenshot,(screenshot_center[0],screenshot_center[1]*2),tuple(head_center_list),(255,255,255),2)
                else:
                    cv2.rectangle(screenshot, (xmin, ymin), (xmax, ymax), (0,255,255), 2)
                

            


                
                centerX = (xmax-xmin)/2+xmin
                centerY = (ymax-ymin)/2+ymin
    
                distance = math.dist([centerX, centerY],[screenshot_center[0],screenshot_center[1]])
                
                

                if int(distance)<closest_part_distance: 
                    
                    closest_part_distance = distance
                    closest_part = i



            except:
                print("",end="")
        


        if keyboard.is_pressed('`'):
            if triggerbot_toggle[0] == True:
                triggerbot = not triggerbot
                print(triggerbot)
                if triggerbot:
                    trigger_label.config(text = "Triggerbot: Active",fg = "green")
                else:
                    trigger_label.config(text = "Triggerbot: Unactive",fg = "red")
                triggerbot_toggle[0] = False
                thread = threading.Thread(target=cooldown, args=(triggerbot_toggle,0.2,))
                thread.start()
                
        elif keyboard.is_pressed('alt'):
            if aim_assist_toggle[0] == True:
                aim_assist = not aim_assist
                print(aim_assist)
                if aim_assist:
                    assist_label.config(text = "Aim Assist: Active",fg = "green")
                else:
                    assist_label.config(text = "Aim Assist: Unactive",fg = "red")
                aim_assist_toggle[0] = False
                thread = threading.Thread(target=cooldown, args=(aim_assist_toggle,0.2,))
                thread.start()

        elif keyboard.is_pressed('p'):
            if silent_aim_toggle[0] == True:
                silent_aim = not silent_aim
                print(silent_aim)
                if silent_aim:
                    silent_label.config(text = "Silent Aim: Active",fg = "green")
                else:
                    silent_label.config(text = "Silent Aim: Unactive",fg = "red")
                silent_aim_toggle[0] = False
                thread = threading.Thread(target=cooldown, args=(silent_aim_toggle,0.2,))
                thread.start()
                
        elif keyboard.is_pressed('up') and no_fov_cooldown[0] == True:
            activation_range += 5
            fov_label.config(text = f"FOV: {activation_range}",fg = "white")
            no_fov_cooldown[0] = False
            thread = threading.Thread(target=cooldown, args=(no_fov_cooldown,0.05,))
            thread.start()
        elif keyboard.is_pressed('down') and no_fov_cooldown[0] == True:
            activation_range -= 5
            fov_label.config(text = f"FOV: {activation_range}",fg = "white")
            no_fov_cooldown[0] = False
            thread = threading.Thread(target=cooldown, args=(no_fov_cooldown,0.05,))
            thread.start()
            
        if keyboard.is_pressed('k'):
            cv2.imwrite(f"tumbnail.jpg", screenshot)  

        if closest_part != -1:
            xmin = df.iloc[closest_part,0]
            ymin = df.iloc[closest_part,1]*1.01
            xmax = df.iloc[closest_part,2]
            ymax = df.iloc[closest_part,3]*1.01
            head_center_list = [int((xmax-xmin)/2+xmin),int((ymax-ymin)/2+ymin)]
            if triggerbot == True and screenshot_center[0] in range(int(xmin),int(xmax)) and screenshot_center[1] in range(int(ymin),int(ymax)):
                shoot()


            if silent_aim == True and silent_aim_not_cooldown[0] == True:


                xdif = (head_center_list[0]-screenshot_center[0])*AIM_SPEED*target_multiply[MONITOR_SCALE]
                ydif = (head_center_list[1]-screenshot_center[1])*AIM_SPEED*target_multiply[MONITOR_SCALE]
                data = f"silent{int(xdif)}:{int(ydif)}"
                serialcomm.write(data.encode())
                silent_aim_not_cooldown[0] = False
                thread = threading.Thread(target=cooldown, args=(silent_aim_not_cooldown,0.2,))
                thread.start()
                


            

            
            # cv2.line(screenshot, (screenshot_center[0],screenshot_center[1]), head_center, (255,255,255), 1) 
            # if screenshot_center[0] not in range(int(xmin),int(xmax)) or screenshot_center[1] not in range(int(ymin),int(ymax)):
            if closest_part_distance < activation_range and aim_assist == True and send_next[0] == True:
                xdif = (head_center_list[0]-screenshot_center[0])*AIM_SPEED*target_multiply[MONITOR_SCALE]
                ydif = (head_center_list[1]-screenshot_center[1])*AIM_SPEED*target_multiply[MONITOR_SCALE]
                data = f"{int(xdif)}:{int(ydif)}"
                serialcomm.write(data.encode())
                send_next[0] = False
                thread = threading.Thread(target=cooldown, args=(send_next,0.05,))
                thread.start()
                # while(serialcomm.readline().decode('ascii') != "done"):
                    # print(serialcomm.readline().decode('ascii'))
                    # continue




            
                

        

        cv2.imshow("frame", screenshot)
        if(cv2.waitKey(1) == ord('q')):
            cv2.destroyAllWindows()
            break

# python yolov5\export.py --weights scripts/best_nano_new.pt --include engine --device 0
# python -u "c:\Users\PyPit\OneDrive\Documents\CODE\Valorant arduino\scripts\main.py"


