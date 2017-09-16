import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib as mlp
import matplotlib.animation as animation
import serial
from pprint import pprint
import re
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


WIDTH = 10
HEIGHT= 4
m = interp1d([-80,-20],[0,1])


#setup serial
serialReader = serial.Serial('/dev/tty.SLAB_USBtoUART', 115200, timeout=1)
serialString = ""

#hide the toolbar :)
mlp.rcParams['toolbar'] = 'None'



data = np.zeros((HEIGHT,WIDTH))
data[0][0] = float(1)


#keeps track of which coloumn to write to for each antenna
dataColIndexes = [0,0,0,0]

def dataToXYZarrays():
    X = []
    Y = []
    Z = []
    for i in range(0,HEIGHT):
        for t in range(0, WIDTH):
            X.append(t)
            Y.append(i)
            Z.append(data[i][t])
    return X,Y,Z

#create a shared window for 4 diagrams

f= plt.figure("Pronto Vision")
ax1 = plt.subplot(221)
ax2 = f.add_subplot(223, projection='3d')
ax3 = plt.subplot(122)

scaleSq = str(int(WIDTH/HEIGHT))
scaleReq = str(int(WIDTH/(HEIGHT*2)))
sem1 = ax1.imshow(data, interpolation='nearest', aspect=scaleReq,
                  cmap='bone')
X,Y,Z = dataToXYZarrays()
sem2 = ax2.plot_trisurf(X,Y,Z, cmap="hot",  shade="true")
sem3 = ax3.imshow(data, aspect=scaleSq,
                                   interpolation='bicubic',
                 cmap='copper', extent=[0, WIDTH, 0, HEIGHT])

def updateFrame(*args):
    global data
    global sem3
    #pprint(data)
    readSerial()
    sem1.set_array(data)
    X, Y, Z = dataToXYZarrays()
    sem2 = ax2.plot_trisurf(X, Y, Z, cmap="hot",shade="true")
    sem3.set_array(data)

def readSerial():
     global serialString
     global data
     serialString += serialReader.read()  # Wait forever for anything
     data_left = serialReader.inWaiting()  # Get the number of characters ready to be read
     serialString += serialReader.read(data_left)
     #print('\n\na: '+ serialString)
     serialString = re.sub(r'[^0-9\.\,\-\:]', '', serialString)
     #print('\nb: '+serialString)
     parseString()

def parseString():
    global serialString
    global dataColIndex
    global dataRowIndex
    global data
    tokens = serialString.split(",")
    if len(tokens) > 1:
        antennaIndexes = []
        tokensFloats = []
        for t in tokens[:len(tokens)-1]:
            fl = -1
            try:
                antennaIndex = int(t[0])
                fl = float(t[2:])
                #interpolate to 0->1
                fl = float(m(fl))
            except ValueError:
                print('parsing error caught\n')
            finally:
                antennaIndexes.append(antennaIndex)
                tokensFloats.append(fl)
        for a in range(0,len(tokensFloats)):
            token = tokensFloats[a]
            antennaIndex = antennaIndexes[a]
            if fl >= 0 and fl <= 1:
                data[antennaIndex][dataColIndexes[antennaIndex]] = token
            dataColIndexes[antennaIndex] += 1
            if dataColIndexes[antennaIndex] >= WIDTH:
                dataColIndexes[antennaIndex] = 0
            serialString = serialString[serialString.find(",")+1:]


ani = animation.FuncAnimation(f, updateFrame, interval=200)


x = np.array([0, WIDTH * 0.25, WIDTH*0.5, WIDTH*0.75, WIDTH])
my_axis_labels = ['0 ft','1 ft','2 ft','3 ft','4 ft']
plt.xticks(x, my_axis_labels)
y = np.array([0,1,2,3,4])
plt.yticks(y, my_axis_labels)
plt.title('Heat Map behind 4ft x 4ft Wall')



plt.show()



