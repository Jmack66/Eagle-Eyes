from cProfile import run
import numpy as np
import cv2
import sys, time, math
import RPi.GPIO as GPIO
from datetime import datetime

trigger_pin = 18
debug = True
keypoints = True
run_time = 30
size = (640,480//2)
result = cv2.VideoWriter('track.mp4', 
                         cv2.VideoWriter_fourcc(*'mp4v'),
                         10, size)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(trigger_pin, GPIO.IN)

#--- Capture the videocamera (this may also be a video or a picture)
cam_1 = cv2.VideoCapture(0)
cam_2 = cv2.VideoCapture(1)

if keypoints:
    orb = cv2.ORB_create(100)


cam_1.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam_1.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cam_1.set(cv2.CAP_PROP_FPS, 30)
cam_2.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam_2.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cam_2.set(cv2.CAP_PROP_FPS, 30)


def KeysAndDraw(frame):
    keys, des = orb.detectAndCompute(frame, None)
    return cv2.drawKeypoints(frame,keys,None)
def CameraLoop(debug):
    ret_left, frame_left = cam_1.read()
    ret_right, frame_right = cam_2.read()
    keyed_left = KeysAndDraw(frame_left)
    keyed_right = KeysAndDraw(frame_right)
    dim = (640//2,480//2)
    frame_left = cv2.resize(keyed_left, dim, interpolation = cv2.INTER_AREA)
    frame_right = cv2.resize(keyed_right, dim, interpolation = cv2.INTER_AREA)
    dual_stream = np.concatenate((frame_left, frame_right), axis=1)
    result.write(dual_stream)
    if debug:
        cv2.imshow('cap',dual_stream)
    return True


start = time.time()
current = start


while current - start < run_time:
    current = time.time()
    if debug:
        state = True
    else:
        state = GPIO.input(trigger_pin)
    if state:
       CameraLoop(debug) 
    else:
        print("Waiting for High")
print("Loop Complete")
cam_1.release()
cam_2.release()
result.release()
cv2.destroyAllWindows()
