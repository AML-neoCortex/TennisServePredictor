import serial
from datetime import datetime
import csv

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

ser = serial.Serial("COM7", 115200)
ser.flushInput()

IMU1 = []
IMU2 = []

IMU = 0
label = 0

while True:
# for ser_bytes in test_input:
    ser_bytes = ser.readline()
    # skip new line chars
    decoded_bytes = str(ser_bytes[0:len(ser_bytes)-2].decode("unicode_escape"))
    print(decoded_bytes)
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
        dt = datetime.now().strftime("%d_%m_%Y_%H-%M-%S")

        file = f"{OUTPUT_NAME}_{dt}.csv"

        with open(file,'w') as f:
            writer = csv.writer(f,delimiter=',')
            writer.writerow(["IMU","index","x_pos","y_pos","z_pos","..."])
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
