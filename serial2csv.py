import serial
import time
import csv

input = {b'24:4c:ab:82:f6:40\r\n'
b'6,0,7,218,40,7,-21,-3,-35,0,0,0,0,0,0,0,0,0,6,0,7\r\n'
b'24:4c:ab:82:f6:40\r\n'
b'6,0,7,218,40,7,-21,-3,-35,0,0,0,0,0,0,0,0,0,6,0,7\r\n'
b'24:4c:ab:82:f6:40\r\n'
b'6,0,7,218,40,7,-21,-3,-35,0,0,0,0,0,0,0,0,0,6,0,7\r\n'
b'24:4c:ab:82:fc:2c\r\n'
b'0,-2,9,358,-2,13,-1,33,-42,0,0,0,0,0,0,0,0,0,0,-2,9\r\n'
b'24:4c:ab:82:fc:2c\r\n'
b'0,-2,9,358,-2,13,-1,33,-42,0,0,0,0,0,0,0,0,0,0,-2,9\r\n'
b'24:4c:ab:82:fc:2c\r\n'
b'0,-2,9,358,-2,13,-1,33,-42,0,0,0,0,0,0,0,0,0,0,-2,9\r\n'
b'24:4c:ab:82:fc:2c\r\n'
b'0,-2,9,358,-2,13,1,31,-43,0,0,0,0,0,0,0,0,0,0,-2,9\r\n'
b'24:4c:ab:82:fc:2c\r\n'
b'0,-2,9,358,-2,13,1,31,-43,0,0,0,0,0,0,0,0,0,0,-2,9\r\n'
b'24:4c:ab:82:fc:2c\r\n'
b'0,-2,9,358,-2,13,1,31,-43,0,0,0,0,0,0,0,0,0,0,-2,9\r\n'
b'24:4c:ab:82:f6:40\r\n'
b'in\r\n'
b'24:4c:ab:82:f6:40\r\n'
b'save\r\n'}

ser = serial.Serial("/dev/cu.usbserial-1430", 115200)
ser.flushInput()

while True:
    ser_bytes = ser.readline()
    # decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
    print(ser_bytes)
    # with open("test_data.csv","a") as f:
    #     writer = csv.writer(f,delimiter=",")
    #     writer.writerow([time.time(),decoded_bytes])
