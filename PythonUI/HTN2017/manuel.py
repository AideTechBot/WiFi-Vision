import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib as mlp
import matplotlib.animation as animation
import serial
from pprint import pprint
import re


WIDTH = 500
HEIGHT= 4
#setup serial
serialReader = serial.Serial('/dev/tty.SLAB_USBtoUART', 9600, timeout=1)
serialString = ""

#hide the toolbar
mlp.rcParams['toolbar'] = 'None'



data = np.zeros((HEIGHT,WIDTH))
data[0][0] = float(1)


dataRowIndex = 0
dataColIndex = 0

#create a seperate window for the projector
fig = plt.figure()
sep = plt.imshow(data, aspect='auto', interpolation='bicubic',
                 cmap='copper', extent=[0, WIDTH, 0, HEIGHT])

#create a shared window for 4 diagrams
'''
f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row')
ax1.imshow(data, interpolation='bicubic', aspect='auto', cmap='bone')
ax2.imshow(data, interpolation='bilinear', aspect='auto')
ax3.imshow(data, interpolation='kaiser', aspect='auto')
ax4.imshow(data, interpolation='sinc', aspect='auto')
'''


def updateFrame(*args):
    global data
    global sep
    #pprint(data)
    readSerial()
    sep.set_array(data)
    return sep

#returns True successfull
def readSerial():
     global serialString
     global data
     serialString += serialReader.read()  # Wait forever for anything
     data_left = serialReader.inWaiting()  # Get the number of characters ready to be read
     serialString += serialReader.read(data_left)
     print('\n\na: '+ serialString)
     serialString = re.sub(r'[^0-9\.\,]', '', serialString)
     print('\nb: '+serialString)
     parseString()

def parseString():
    global serialString
    global dataColIndex
    global dataRowIndex
    global data
    tokens = serialString.split(",")
    if len(tokens) > 1:
        tokensFloats = [float(t) for t in tokens[:len(tokens)-1]]
        for token in tokensFloats:
            data[dataColIndex][dataRowIndex] = token
            dataColIndex += 1
            if dataColIndex >=HEIGHT:
                dataColIndex= 0
                dataRowIndex += 1
                if dataRowIndex >= WIDTH:
                    dataRowIndex = 0
            serialString = serialString[serialString.find(",")+1:]


ani = animation.FuncAnimation(fig, updateFrame, interval=200)


x = np.array([0, WIDTH * 0.25, WIDTH*0.5, WIDTH*0.75, WIDTH])
my_axis_labels = ['0 ft','1 ft','2 ft','3 ft','4 ft']
plt.xticks(x, my_axis_labels)
y = np.array([0,1,2,3,4])
plt.yticks(y, my_axis_labels)
plt.title('Heat Map behind 4ft x 4ft Wall')
plt.show()



