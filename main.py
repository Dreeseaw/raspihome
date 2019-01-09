# William Dreese
# RasPi Security / Music Cam
# main.py
# 
# python3 main.py <PRE-SLEEP (SECS)>

import sys
import subprocess
import datetime
#import cv2
from picamera import PiCamera
import picamera.array
from time import sleep

def music():
    #get all mp3s from music dir, pick at random
    subprocess.check_call(['omxplayer','high.mp3','&'])

def intruder(frame):
    save_line = "image/temp.png"
    email = "wdreese123@gmail.com"
    cv2.imwrite(save_line, frame)
    subprocess.check_call(['mpack','-s','"Intruder Alert"',save_line,email])
    subprocess.check_call(['rm',save_line])

def trigger(now, frame):
    print("event triggered at %d:%d:%d on %d", now.hour, now.minute,
            now.second, now.weekday())

    if now.weekday() in [0,2,4]: #monday, wed, fri
        if now.hour == 12 and now.minute < 30: return music()
        elif now.hour == 13 and now.minute < 30: return music()
    elif now.weekday() in [1,3]: #tuesday, thursday
        if now.hour == 10 and now.minute > 20 and now.minute < 40: 
            return music()
        elif now.hour == 11 and now.minute > 50 or now.hour == 12 and now.minute < 20: 
            return music()
        elif now.hour == 16 and now.minute > 20 and now.minute < 50: 
            return music()
    return intruder(frame)

def run():

    trig_sleep = 100
    thres = 50

    cam = PiCamera()
    cam.start_preview()
    sleep(5)
    stream = picamera.array.PiRGBArray(cam)

    #fgbg = cv2.createBackgroundSubtractorMOG()

    for x in range(10000):
        #get picamera still image
        cam.capture(stream, format='bgr')
        frame = stream.array
        #fgmask = fgbg.apply(frame)
        print(frame)
        if np.sum(fgmask) > thres and trig_sleep < 0:
            trig_sleep = 100
            trigger(datetime.datetime.now(), frame)
        trig_sleep -= 1

if __name__ == "__main__":
    if len(sys.argv) == 1: run(0)
    else: run(int(sys.argv[1]))

