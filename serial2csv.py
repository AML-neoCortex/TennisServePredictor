import serial
from datetime import datetime
import csv
from imutils.video import VideoStream
import numpy as np

import cv2
import imutils
import time

import csv
import serial
import os
import pickle
from tkinter import *
import pandas as pd

def set_color(serve):
   if serve:
       root.configure(background = ['green'])
   else:
       root.configure(background = ['red'])

INFERENCE = False

OUTPUT_NAME = "data/SERVE"

ser = serial.Serial("COM4", 115200)
ser.flushInput()

IMU1 = []
IMU2 = []

IMU = 0
label = 0
index = 0

# change these boundaries based on what you are tracking
# use the rangedetector.py to find them
trackLower = (0, 217, 121)
trackUpper = (50, 255, 255)

# amount of frames to capture
buffer = 150 
frame_skip = 1

# webcam file data 
filename = ""
webcamFileName = ""

# start webcam feed, modify src if multiple are connected
vs = VideoStream(src=0).start()
# allow the webcamera to warm up
time.sleep(2.0)

while True:
    ser_bytes = ser.readline()
    # skip new line chars
    decoded_bytes = str(ser_bytes[0:len(ser_bytes)-2].decode("unicode_escape"))
    print(decoded_bytes)


    if decoded_bytes == 'sync':

        # use same timestamp for both
        filename = datetime.now().strftime("%d_%m_%Y_%H-%M-%S")
        webcamFileName = f"{OUTPUT_NAME}_{filename}_webcam.csv"

        fileWebcam = open(webcamFileName, mode='w', newline='')
        writerWebcam = csv.writer(fileWebcam)

        rawBallPos = []
        absDifBallPos = []
        frameCount = 1

        for x in range(buffer):

            # skip frames (optional)
            if  not (frameCount % frame_skip == 0):
                continue

            # grab the current frame
            frame = vs.read()
        

            # preprocess frame:
            # resize the frame, blur it, and convert it to the HSV  color space
            frame = imutils.resize(frame, width=600)
            blurred = cv2.GaussianBlur(frame, (11, 11), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

            # construct a mask from HSV threshold values, then erode and dilate to remove artifacts
            mask = cv2.inRange(hsv, trackLower, trackUpper)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            # find contours in the mask and initialize the current (x, y) center of the ball
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            
            # hard code answer if nothing is detected to stop program crashes
            center = (0,0)

            # only proceed if at least one contour was found
            if len(cnts) > 0:

                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])) 

                print(center)

                # only proceed if the radius meets a minimum size to remove artifacts 
                if radius > 10:
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    cv2.circle(frame, (int(x), int(y)), int(radius),
                        (0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)

            rawBallPos.append(center)

            # display tracking
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
            # if the 'q' key is pressed, stop the loop
            if key == ord("q"):
                break

        # calc diff in abs movement from first frame 
        initPos = rawBallPos[0]
        
        # check more rawballpos is more than 0 len 
        for pos in rawBallPos[1:]:
            absDifBallPos.append(tuple(x-y for x,y in zip(initPos,pos)))

        print(absDifBallPos)

        # write data to csv 
        for i in range(buffer-1):
            row = [i, absDifBallPos[i][0],absDifBallPos[i][1]]
            writerWebcam.writerow(row)

        fileWebcam.close()

        # sync data collection with IMU
        time.sleep(0.01)

    # Get MAC address
    if decoded_bytes == "24:4c:ab:82:fc:2c":
        IMU = 2
    elif decoded_bytes == "24:4c:ab:82:f6:40":
        IMU = 1
    # 7 Vars x 3 DoF
    elif len(decoded_bytes.split(',')) == 21:
        data = [int(x) for x in decoded_bytes.split(',')]
        match IMU:
            case 1:
                IMU1.append(data)
            case 2:
                IMU2.append(data)
    # Add label
    elif decoded_bytes == "in":
        label = 1
    elif decoded_bytes == "out":
        label = 0

    # TO save or not to save? That is the question...
    if decoded_bytes == "save":
        # Append to output file

        file = f"{OUTPUT_NAME}_{filename}.csv"

        with open(file,'w') as f:
            writer = csv.writer(f,delimiter=',')
            writer.writerow(['IMU','index','Xacc', 'Yacc', 'Zacc', 'Xori', 'Yori', 'Zori', 'Xmag', 'Ymag' , 'Zmag', 'Xgyro', 'Ygyro', 'Zgyro', 'Xrot','Yrot', 'Zrot' , 'Xlin' ,'Ylin', 'Zlin', 'Xgrav', 'Ygrav', 'Zgrav'])
            # Write label on first row
            writer.writerow([label])
            # Append IMU1
            for i in range(len(IMU1)):
                # Append index at beggining of row
                IMU1[i].insert(0,i)
                # And IMU label
                IMU1[i].insert(0,1)
                writer.writerow(IMU1[i])
            # Append IMU2
            for i in range(len(IMU2)):
                # Append index at beggining of row
                IMU2[i].insert(0,i)
                # And IMU label
                IMU2[i].insert(0,2)
                writer.writerow(IMU2[i])
        # Clear buffer lists
        IMU1 = []
        IMU2 = []

        if INFERENCE:
            labels = ['IMU','index','Xacc', 'Yacc', 'Zacc', 'Xori', 'Yori', 'Zori', 'Xmag', 'Ymag' , 'Zmag', 'Xgyro', 'Ygyro', 'Zgyro', 'Xrot','Yrot', 'Zrot' , 'Xlin' ,'Ylin', 'Zlin', 'Xgrav', 'Ygrav', 'Zgrav']
            df_imu = pd.read_csv(file,skiprows=4,header=None,names=labels)
            df_cam = pd.read_csv(webcamFileName,names=['index','x','y'])

            df = pd.merge(df_imu, df_cam, on='index')

            df_imu1 = df.loc[df['IMU'] == 1]
            df_imu1.columns = ['IMU','index','X1acc', 'Y1acc', 'Z1acc', 'X1ori', 'Y1ori', 'Z1ori', 'X1mag', 'Y1mag' , 'Z1mag', 'X1gyro', 'Y1gyro', 'Z1gyro', 'X1rot','Y1rot', 'Z1rot' , 'X1lin' ,'Y1lin', 'Z1lin', 'X1grav', 'Y1grav', 'Z1grav', 'Xcam', 'Ycam']
            df_imu2 = df.loc[df['IMU'] == 2]
            df_imu2.columns = ['IMU','index','X2acc', 'Y2acc', 'Z2acc', 'X2ori', 'Y2ori', 'Z2ori', 'X2mag', 'Y2mag' , 'Z2mag', 'X2gyro', 'Y2gyro', 'Z2gyro', 'X2rot','Y2rot', 'Z2rot' , 'X2lin' ,'Y2lin', 'Z2lin', 'X2grav', 'Y2grav', 'Z2grav', 'Xcam', 'Ycam']

            merged_df = pd.merge(df_imu1, df_imu2, on='index')
            merged_df.drop(columns=['index', 'IMU_x'], inplace=True)

            serve_data = np.array(merged_df.to_numpy())

            print(f'Data Loaded. {serve_data.shape}')

            model_file = '/models/rf.sav'
            model = pickle.load(open(model_file, 'rb'))

            print('Pre-trained model weights loaded.')

            root = Tk()
            root.title("Serve In or Out")
            root.resizable(False, False)
            root.attributes("-fullscreen", True)

            serve = model.predict(np.array([serve_data]).reshape(1, -1))[0]
            print(f'Serve outcome predicted: {serve}')

            set_color(serve)

            root.mainloop()
            
        
    elif decoded_bytes == "nosave":
        # Clear buffer lists
        IMU1 = []
        IMU2 = []

        # delete webcam data using last save file name
        os.remove(webcamFileName)
