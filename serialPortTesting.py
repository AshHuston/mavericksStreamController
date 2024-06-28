import serial
from serial import tools
from serial.tools import list_ports
import time
import struct

ports = list_ports.comports(include_links=True)
print(ports[0].device)
with serial.Serial() as ser:
    ser.timeout = 0.005
    ser.baudrate = 9600
    ser.port = ports[0].device
    ser.open()
    while True:
        if ser.readable:
            serialData = ser.readline()
            if str(serialData) != "b''":
                serialData = int(serialData.decode())
            else:
                serialData = 0
        else:
            serialData = "ERROR"
        print(serialData)
        time.sleep(.25)
    ser.close()

#b'213\r\n'

'''
ser = serial.Serial('/dev/ttyUSB0')  # open serial port
print(ser.name)         # check which port was really used
ser.write(b'hello')     # write a string
ser.close()    
'''