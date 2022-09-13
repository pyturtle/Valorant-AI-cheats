import cv2
import os

if __name__ == "__main__":
    video_folder = r"C:\Users\PyPit\OneDrive\Desktop\cheats\videos"
    export_folder = r"C:\Users\PyPit\OneDrive\Desktop\cheats\exported frames"


    os.chdir(export_folder)# changes directory to exports
    MONITOR_WIDTH = 1920#game res
    MONITOR_HEIGHT = 1080#game res


    MONITOR_SCALE = 5#how much the screen shot is downsized by eg. 5 would be one fifth of the monitor dimensions
    region = (int(MONITOR_WIDTH/2-MONITOR_WIDTH/MONITOR_SCALE/2),int(MONITOR_HEIGHT/2-MONITOR_HEIGHT/MONITOR_SCALE/2),int(MONITOR_WIDTH/2+MONITOR_WIDTH/MONITOR_SCALE/2),int(MONITOR_HEIGHT/2+MONITOR_HEIGHT/MONITOR_SCALE/2))
    x,y,width,height = region

    for video_name in os.listdir(video_folder):
        vidcap = cv2.VideoCapture(video_folder+"\\"+video_name)#assigning current video
        success, image = vidcap.read()# reads in a frame
        count = 0
        frame = 0   
        while success:
            frame += 1
            success, image = vidcap.read()
            if (frame % 20 == 0):# only activates every 20 frames
                image = image[y:height,x:width]#crops image to scale cordinates
                cv2.imwrite(video_name+"frame%d.jpg" % count, image)     # save frame as JPEG file
                success, image = vidcap.read()
                print('Read a new frame: ', success)
                count += 1#amount of frames
    