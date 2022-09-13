import cv2
import os
import torch
from mss import mss
import time
import numpy as np

def cooldown(cooldown_bool,wait):
    #cooldown threed for toggels or cooldowns
    time.sleep(wait)
    cooldown_bool[0] = True



if __name__ == "__main__":
    file_name = "icebox_"
    img_output =  r"C:\Users\PyPit\OneDrive\Desktop\Auto_ano\dataset\images\train"# image output path
    label_output = r"C:\Users\PyPit\OneDrive\Desktop\Auto_ano\dataset\labels\train"# label output path
    img_num = 0# img count
    MONITOR_WIDTH = 1920#base res
    MONITOR_HEIGHT = 1080#base res
    MONITOR_SCALE = 5#how much the screen shot is downsized by eg. 5 would be one fifth of the monitor dimensions
    region = (int(MONITOR_WIDTH/2-MONITOR_WIDTH/MONITOR_SCALE/2),int(MONITOR_HEIGHT/2-MONITOR_HEIGHT/MONITOR_SCALE/2),int(MONITOR_WIDTH/2+MONITOR_WIDTH/MONITOR_SCALE/2),int(MONITOR_HEIGHT/2+MONITOR_HEIGHT/MONITOR_SCALE/2))
    x,y,width,height = region
    x_length = (width-x) # screenshot length
    y_length = (height-y) # screenshot lenght
    model = torch.hub.load(r'C:\Users\PyPit\OneDrive\Documents\CODE\Valorant_arduino\yolov5', 'custom', path=r"C:\Users\PyPit\OneDrive\Documents\CODE\Valorant_arduino\scripts\best.pt", source='local')#loading model onto gpu
    model.conf = 0.40# model confidance threshold
    model.iou = 0.65# overlap threshhold threshold
    model.maxdet = 10# max detections
    model.amp = True# amps model 
    save_cooldown = [True]
    success = False
    print(region)
    with mss() as sct:
        while True:
            if save_cooldown[0]:#makes sure not on cooldown
                screenshot = np.array(sct.grab(region))
                df= model(screenshot, size=640).pandas().xyxy[0]# runs model
                lines = []# txt lines list
                for i in range(0,10):
                    try:
                        xmin = int(df.iloc[i,0])
                        ymax = (int(df.iloc[i,3]))
                        ymin = abs(int(df.iloc[i,1]) - ymax)/y_length# these devisions are for the yolov5 txt format
                        xmax = abs((int(df.iloc[i,2]))-xmin)/x_length
                       
                        ymax /= y_length
                        xmin /= x_length

                        xmin += xmax/2#slight ajustments idk why its needed but the cords are fucked up if its not there
                        ymax -= ymin/2
                        line = f"{int(df.iloc[i,5])} {xmin} {ymax} {xmax} {ymin}\n"# makes txt line
                        lines.append(line)
                        print(img_num)# prints for every detection
                        success = True
                        

                        


                    


                        
                        


                    except Exception as e:# the exception is to print nothing
                        print("", end="")
                        # print(e)
                if success:
                    with open(f'{label_output}\\{file_name}_{img_num}.txt', 'w') as f: #writes to txt file
                        for line in lines:
                            f.write(line)
                    cv2.imwrite(f"{img_output}\\{file_name}_{img_num}.jpg", screenshot) # saves img
                    img_num += 1
                    save_cooldown[0] = False#cooldown starts and call the cooldown function
                    cooldown(save_cooldown,0.5)
                    
                success = False
            cv2.imshow("frame", screenshot)
            if(cv2.waitKey(1) == ord('q')):
                cv2.destroyAllWindows()
                break
       
        

        
