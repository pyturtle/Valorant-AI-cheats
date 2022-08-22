import torch
import cv2
import numpy as np
import mss.tools
# from mss import mss
import win32api
import win32con
import win32gui
import win32ui
import math
import keyboard
import time
import threading


ACTIVATION_RANGE = 500
def grab_screen(region=None):
    hwin = win32gui.GetDesktopWindow()
 
    if region:
        left, top, x2, y2 = region
        widthScr = x2 - left + 1
        heightScr = y2 - top + 1
    else:
        widthScr = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        heightScr = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
 
    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, widthScr, heightScr)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (widthScr, heightScr), srcdc, (left, top), win32con.SRCCOPY)
 
    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype='uint8')
    img.shape = (heightScr, widthScr, 4)
 
    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())
 
    return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)


def cooldown(cooldown_bool,wait):
    time.sleep(wait)
    cooldown_bool[0] = True

def shoot(can_shoot):
    if can_shoot[0] == True:
        keyboard.press_and_release("j")
        print ("shoot")
        can_shoot[0] = False
        thread = threading.Thread(target=cooldown, args=(can_shoot,0.220,))
        thread.start()






if __name__ == "__main__":
    """
    Main part  of the program
    """
    can_shoot = [True]
    triggerbot = False
    triggerbot_toggle = [True]
    model = torch.hub.load(r'C:\Users\PyPit\OneDrive\Documents\CODE\Valorant arduino\scripts\yolov5-master', 'custom', path=r"C:\Users\PyPit\OneDrive\Documents\CODE\Valorant arduino\scripts\best.pt", source='local').cuda() # load model
    monitor_width = 1920
    monitor_height = 1080
    monitor_scale = 4#ss size for scaling
    region = (int(monitor_width/2-monitor_width/monitor_scale/2),int(monitor_height/2-monitor_height/monitor_scale/1.5),int(monitor_width/2+monitor_width/monitor_scale/2),int(monitor_height/2+monitor_height/monitor_scale/1.5))
    x,y,width,height = region
    screenshot_center = [int((width-x)/2),int((height-y)/2)]


    print(region)



    #(int(monitor_width/2-monitor_width/monitor_scale/2),int(monitor_height/2-monitor_height/monitor_height/2),int(monitor_width/2+monitor_width/monitor_scale/2),int(monitor_height/2+monitor_height/monitor_height/2))
    #(730,360,1190,710)
    #{"top": 350, "left": 640, "width": 640, "height":400}

    while(True):
        screenshot = np.array(grab_screen(region = region)).cuda()
        results = model(screenshot, size=640)
        df= results.pandas().xyxy[0]
        closest = 1000000
        closest_head = None
        distances = []
        
        for i in range(0,20):
            try:
                xmin = int(df.iloc[i,0])
                ymin = int(df.iloc[i,1])
                xmax = int(df.iloc[i,2])
                ymax = int(df.iloc[i,3])


                if int(df.iloc[i,5]) == 0:
                    cv2.rectangle(screenshot, (xmin, ymin), (xmax, ymax), (255,0,0), 2)


                elif int(df.iloc[i,5]) == 1:

                    cv2.rectangle(screenshot, (xmin, ymin), (xmax, ymax), (0,0,255), 2)
                    
                    centerX = (xmax-xmin)/2+xmin
                    centerY = (ymax-ymin)/2+ymin
        
                    distance = math.dist([centerX, centerY],[230,175])



                    if int(distance)<closest: 
                        closest = distance
                        closest_head = i

                    # cv2.circle(screenshot, center, 3000 ,(0,0,255), -1)

            except:
                print("",end="")
        
        if keyboard.is_pressed('alt'):
            if triggerbot_toggle[0] == True:
                triggerbot = not triggerbot
                print(triggerbot)
                triggerbot_toggle[0] = False
                thread = threading.Thread(target=cooldown, args=(triggerbot_toggle,0.5,))
                thread.start()

        if closest_head:
            xmin = int(df.iloc[closest_head,0])
            ymin = int(df.iloc[closest_head,1])
            xmax = int(df.iloc[closest_head,2])
            ymax = int(df.iloc[closest_head,3])
            center = (int((xmax-xmin)/2+xmin),int((ymax-ymin)/2+ymin))
            cv2.line(screenshot, (screenshot_center[0],screenshot_center[1]), center, (255,255,255), 2) 
            if screenshot_center[0] in range(xmin,xmax) and screenshot_center[1] in range(ymin,ymax) and triggerbot == True:
                shoot(can_shoot)
                
 
                

        cv2.imshow("frame", screenshot)
        if(cv2.waitKey(1) == ord('q')):
            cv2.destroyAllWindows()
            break

# python scripts\yolov5-master\export.py --weights scripts/best.pt --include engine --device 0