import serial
from datetime import datetime
import csv

input = [b'24:4c:ab:82:f6:40\r\n',
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

OUTPUT_NAME = "test_data.csv"

# ser = serial.Serial("/dev/cu.usbserial-1430", 115200)
# ser.flushInput()

IMU1 = []
IMU2 = []

IMU = 0
label = 0

# while True:
    # ser_bytes = ser.readline()
# Append to output file
with open(OUTPUT_NAME,"a") as f:
    writer = csv.writer(f,delimiter=",")
    for ser_bytes in input:
        # skip new line chars
        decoded_bytes = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
        # print(decoded_bytes)
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
        elif decoded_bytes == "in":
            label = 1
        elif decoded_bytes == "out":
            label = 0

        if decoded_bytes == "save":
            # print(IMU1)
            # print(IMU2)
            dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            writer.writerow([dt,"IMU1",IMU1])
            writer.writerow([dt,"IMU2",IMU2])
