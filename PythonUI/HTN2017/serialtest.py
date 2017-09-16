import serial
import time

s = serial.Serial('/dev/tty.SLAB_USBtoUART', 9600, timeout=1)

while 1:
     tdata = s.read()  # Wait forever for anything
     time.sleep(1)  # Sleep (or inWaiting() doesn't give the correct value)
     data_left = s.inWaiting()  # Get the number of characters ready to be read
     tdata += s.read(data_left)
     print (tdata)
     print '\n'