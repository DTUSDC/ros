import serial
import struct
s1 = 0
port = serial.Serial("/dev/ttyUSB0", 9600)
while True: 
    s1 = int(input())
    print(s1)
    my_ans = struct.pack("B",s1)
    port.write(my_ans)
port.close()
