import serial
from datetime import datetime
import csv
from collections import deque
from imutils.video import VideoStream
import numpy as np

import cv2
import imutils
import time

import csv
import serial
import os 

test_input = [b'24:4c:ab:82:f6:40\r\n',
b'6,0,7,218,40,7,-21,-3,-35,0,0,0,0,0,0,0,0,0,6,0,7\r\n',
b'24:4c:ab:82:f6:40\r\n',
b'6,0,7,218,40,7,-21,-3,-35,0,0,0,0,0,0,0,0,0,6,0,7\r\n',
b'24:4c:ab:82:f6:40\r\n',
b'6,0,7,218,40,7,-21,-3,-35,0,0,0,0,0,0,0,0,0,6,0,7\r\n',
b'24:4c:ab:82:fc:2c\r\n',
b'0,-2,9,358,-2,13,-1,33,-42,0,0,0,0,0,0,0,0,0,0,-2,9\r\n',
b'24:4c:ab:82:fc:2c\r\n',
b'0,-2,9,358,-2,13,-1,33,-42,0,0,0,0,0,0,0,0,0,0,-2,9\r\n',
b'24:4c:ab:82:fc:2c\r\n',
b'0,-2,9,358,-2,13,-1,33,-42,0,0,0,0,0,0,0,0,0,0,-2,9\r\n',
b'24:4c:ab:82:fc:2c\r\n',
b'0,-2,9,358,-2,13,1,31,-43,0,0,0,0,0,0,0,0,0,0,-2,9\r\n',
b'24:4c:ab:82:fc:2c\r\n',
b'0,-2,9,358,-2,13,1,31,-43,0,0,0,0,0,0,0,0,0,0,-2,9\r\n',
b'24:4c:ab:82:fc:2c\r\n',
b'0,-2,9,358,-2,13,1,31,-43,0,0,0,0,0,0,0,0,0,0,-2,9\r\n',
b'24:4c:ab:82:f6:40\r\n',
b'in\r\n',
b'24:4c:ab:82:f6:40\r\n',
b'save\r\n']

OUTPUT_NAME = "data/SERVE"

ser = serial.Serial("COM4", 115200)
ser.flushInput()

IMU1 = []
IMU2 = []

IMU = 0
label = 0

# trackLower = (24, 49, 90)
# trackUpper = (90,160,255)
trackLower = (0, 217, 121)
trackUpper = (50, 255, 255)

buffer = 150 # amount of frames to capture
frame_skip = 1
index = 0
# webcam data 
filename = ""
webcamFileName = ""




# pts = deque(maxlen=buffer)
vs = VideoStream(src=0).start()
# vs = cv2.VideoCapture(0, cv2.CAP_MSMF)VideoStream(src=0,cv2.CAP_MSMF).start()
# vs = cv2.VideoCapture(0, cv2.CAP_MSMF)
# connection to serial, TO CHANGE based on user machine
# ser = serial.Serial("dev/cu.usbserial-1430", 115200)
# ser.flushInput()

# allow the camera or video file to warm up
time.sleep(2.0)
while True:
# for ser_bytes in test_input:
    ser_bytes = ser.readline()
    # skip new line chars
    decoded_bytes = str(ser_bytes[0:len(ser_bytes)-2].decode("unicode_escape"))
    print(decoded_bytes)


    if decoded_bytes == 'sync':

        filename = datetime.now().strftime("%d_%m_%Y_%H-%M-%S")


        webcamFileName = f"{OUTPUT_NAME}_{filename}_webcam.csv"

        # Write column headers based on number of coordinates
        # header_row = ["Index"]
        # for i in range(buffer):
        #     header_row.append(f"X Coordinate {i}")
        #     header_row.append(f"Y Coordinate {i}")
        fileWebcam = open(webcamFileName, mode='w', newline='')
        writerWebcam = csv.writer(fileWebcam)
        # writerWebcam.writerow(header_row)
        # file.close()


        # file = open(filename, mode='a', newline='')
        # writer = csv.writer(file)
        rawBallPos = []
        absDifBallPos = []
        frameCount = 1
        # maybe only take one frame out of x 
        for x in range(buffer):

            # skip x frames
            if  not (frameCount % frame_skip == 0):
                continue
            # grab the current frame
            frame = vs.read()
        

            # resize the frame, blur it, and convert it to the HSV
            # color space
            frame = imutils.resize(frame, width=600)
            blurred = cv2.GaussianBlur(frame, (11, 11), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
            # construct a mask for the color "green", then perform
            # a series of dilations and erosions to remove any small
            # blobs left in the mask
            mask = cv2.inRange(hsv, trackLower, trackUpper)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

                # find contours in the mask and initialize the current
            # (x, y) center of the ball
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
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
                # if center is None:
                # 	center = (0,0)
                # only proceed if the radius meets a minimum size
                if radius > 10:
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    cv2.circle(frame, (int(x), int(y)), int(radius),
                        (0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)
            # update the points queue
            # pts.appendleft(center)
            rawBallPos.append(center)

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

        # print(rawBallPos)	
        print(absDifBallPos)

        # # maybe normalize?
        # data_transposed = list(zip(*absDifBallPos))
        # print(data_transposed)
        # # add index
        # data_transposed.insert(0,index)
        # # Write coordinate data as rows
        # for data in data_transposed:
        # 	writer.writerow(data)


        # Write coordinate data as a single row
        # row = [index]
        # for coord in absDifBallPos:
        #     row += list(coord)
        # writerWebcam.writerow(row)

        for i in range(buffer-1):
            row = [i, absDifBallPos[i][0],absDifBallPos[i][1]]
            writerWebcam.writerow(row)

        
        # index += 1
        fileWebcam.close()

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
        # dt = datetime.now().strftime("%d_%m_%Y_%H-%M-%S")

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
        
    elif decoded_bytes == "nosave":
        # Clear buffer lists
        IMU1 = []
        IMU2 = []
        os.remove(webcamFileName)
    

vs.stop()
cv2.destroyAllWindows()