import serial
from serial import tools
from serial.tools import list_ports
import time

global connectedControllerPort
connectedControllerPort = None

#controllerIsConnected = False
connectionFound = False

while True:
    print("-----------------------------------------")
    time.sleep(3)
    ports = list_ports.comports(include_links=True)
    i = 0
    for any in ports:
        i += 1
        print(f'{i}.  pid  {any.pid}')
        print(f'{i}.  vid  {any.vid}')
        print(f'{i}.  manufacturer  {any.manufacturer}')
        print("----------------")
        '''
        if any.serial_number.count("arduino uno") >= 1:
            controllerIsConnected = True
            connectionFound = True
            if connectedControllerPort.is_open == False:
                connectedControllerPort.timeout = 0.005
                connectedControllerPort.baudrate = 9600
                connectedControllerPort.port = any.device
                try:
                    connectedControllerPort.open()
                except:
                    pass
        '''