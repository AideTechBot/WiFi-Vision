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
from random import randint
from copy import copy, deepcopy

from matplotlib.widgets import Button


class Callback(object):

    def onStartPressed(self, event):
        print 'start pressed'
        global serialRW
        serialRW.write("G".encode())

    def useAsBaseline(self, event):
        print 'base pressed'
        global baseline
        global data
        baseline = deepcopy(data)
        cmpDataToBaseline()

    def turn(self, event):
        global serialRW
        serialRW.write("H".encode())
        print 'turn pressed'

        global mode
        global dataColIndexes
        mode = 1
        for u in range(0, len(dataColIndexes)):
            dataColIndexes[u] = 99

    def end(self, event):
        print 'finished pressed'
        global mode
        global dataColIndexes
        mode = 0
        for u in range(0, len(dataColIndexes)):
            dataColIndexes[u] = 0
        if baseline is not None:
            cmpDataToBaseline()
            X, Y, Z = dataToXYZarrays(baseline)
        else:
            X, Y, Z = dataToXYZarrays(data)
        global ax2
        ax2.plot_trisurf(X, Y, Z, cmap="hot", shade="true")


#constants
WIDTH = 100 #(num increments on track)
HEIGHT= 6 #(num antennas)
REDRAW_INTERVAL = 20
OUTER_INPUT_RANGE = [10.0,80.0]
INPUT_RANGE = [30.0,60.0]
DEPTH_IN_Z = True #If false, depth in Y
#ONLY_DRAW_3D_ON_COMPLETE = True
TURN_OFF_PROJECTION = True

#global vars
m = interp1d(INPUT_RANGE,[0,1])
serialString = ""
scaleSq = str(int(WIDTH/HEIGHT))
scaleReq = str(int(WIDTH/(HEIGHT*2)))

#setup serial
#Arduino Uno
serialRW = serial.Serial('/dev/tty.usbmodem1411', 115200, timeout=1)
#esp8266
#serialReader = serial.Serial('/dev/tty.SLAB_USBtoUART', 115200, timeout=1)
serialRW.close()
serialRW.open()
serialRW.flush()
serialRW.write("1".encode())


baseline = None

data = np.zeros((HEIGHT,WIDTH))
#I think it uses the initial range in data points as a the permanent range
#needs the '1' to get the full scale
data[0][0] = float(1)


#Keeps track of which coloumn to write to for each antenna
dataColIndexes = [0]*HEIGHT

#0
#1
mode = 0


#hide the toolbar
mlp.rcParams['toolbar'] = 'None'

#for 3D map, turns 2D data array (x,y)->z into three 1D parallel arrays
def dataToXYZarrays(ddta):
    X = []
    Y = []
    Z = []
    for i in range(0,HEIGHT):
        for t in range(0, WIDTH):
            X.append(t)
            Y.append(i)
            Z.append(ddta[i][t])
    if DEPTH_IN_Z:
        return X, Y, Z
    else:
        return X, Z, Y


def cmpDataToBaseline():
    for i in range(0,HEIGHT):
        for t in range(0, WIDTH):
            temp = (baseline[i][t] - data[i][t])
            print(str(temp))
            temp = temp * 3
            if temp > 1:
                data[i][t] = 1
            elif temp < 0:
                data[i][t] = 0
            else:
                data[i][t] = temp


# create a shared window (figure) using subplots
f = plt.figure("Pronto Vision")
ax1 = plt.subplot(221)
ax1.set_title('Unprocessed Readings')
ax2 = f.add_subplot(223, projection='3d')
ax2.set_title('3D Visualization')
ax3 = plt.subplot(122)
ax3.set_title('Heat Map behind 4ft x 4ft Wall')

callback = Callback()
plt.subplots_adjust(bottom=0.2)
axprev = plt.axes([0.85, 0.05, 0.1, 0.075])
axturn = plt.axes([0.55, 0.05, 0.1, 0.075])
axend = plt.axes([0.7, 0.05, 0.1, 0.075])
axnext = plt.axes([0.4, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Start Reading')
bnext.on_clicked(callback.onStartPressed)
bturn = Button(axturn, 'Turn')
bturn.on_clicked(callback.turn)
bend = Button(axend, 'Finish')
bend.on_clicked(callback.end)
bprev = Button(axprev, 'Use as baseline')
bprev.on_clicked(callback.useAsBaseline)


#create projection window
if not TURN_OFF_PROJECTION:
    f2 = plt.figure("Projected Readings")
    ax4 = plt.subplot(111)


#set up axes on Heat Map
x_axis_points = np.array([0, WIDTH * 0.25, WIDTH*0.5, WIDTH*0.75, WIDTH])
y_axis_points = np.array([0, HEIGHT * 0.25, HEIGHT*0.5, HEIGHT*0.75, HEIGHT])
my_axis_labels = ['0 ft','1 ft','2 ft','3 ft','4 ft']
plt.sca(ax3)
plt.xticks(x_axis_points, my_axis_labels)
plt.yticks(y_axis_points, my_axis_labels)

#turn off other axes
ax1.set_axis_off()
ax2.set_axis_off()
if not TURN_OFF_PROJECTION:
    ax4.set_axis_off()

#initial renders
sem1 = ax1.imshow(data, interpolation='nearest', aspect=scaleReq,
                  extent=[0, WIDTH, 0, HEIGHT], cmap='bone')

X,Y,Z = dataToXYZarrays(data)
ax2.plot_trisurf(X,Y,Z, cmap="hot", shade="true")

sem3 = ax3.imshow(data, aspect=scaleSq, interpolation='bilinear',
                  extent=[0, WIDTH, 0, HEIGHT], cmap='plasma')

if not TURN_OFF_PROJECTION:
    sem4 = ax4.imshow(data, interpolation='bilinear', aspect='auto',
                      extent=[0, WIDTH, 0, HEIGHT], cmap='binary')



def updateFrame(*args):
    #pprint(data)
    readSerial()
    global sem1
    global sem3
    sem1.set_array(data)
    sem3.set_array(data)

def updateFrame2(*args):
    global sem4
    sem4.set_array(data)

def readSerial():
     global serialString
     global data
     serialString += serialRW.read()  # Wait forever for anything
     data_left = serialRW.inWaiting()  # Get the number of characters ready to be read
     serialString += serialRW.read(data_left)
     #print('\n\na: '+ serialString)
     serialString = re.sub(r'[^0-9\.\,\-\:]', '', serialString)
     #print('\nb: '+serialString)
     parseString()




def parseString():
    global serialString
    global data
    global mode
    global dataColIndexes
    tokens = serialString.split(",")
    if len(tokens) > 1:
        antennaIndexes = []
        tokensFloats = []
        for t in tokens[:len(tokens)-1]:
            fl = -1
            antennaIndex = -1
            try:
                antennaIndex = 6 - int(t[0]) #1-6 input, want 5-0
                fl = float(t[2:])
                #interpolate to 0->1
                if OUTER_INPUT_RANGE[0] <= fl <= INPUT_RANGE[0]:
                    fl = INPUT_RANGE[0]+0.1
                if OUTER_INPUT_RANGE[1] >= fl >= INPUT_RANGE[1]:
                    fl = INPUT_RANGE[1] -0.1
                print fl
                fl = 1 - float(m(fl))
            except ValueError:
                print(serialString)
                print('parsing error caught\t' + str(t))
                fl = -1
                antennaIndex = -1
            except IndexError:
                print(serialString)
                print('parsing error caught\t' + str(t))
                fl = -1
                antennaIndex = -1
            finally:
                antennaIndexes.append(antennaIndex)
                tokensFloats.append(fl)
        for a in range(0,len(tokensFloats)):
            serialString = serialString[serialString.find(",") + 1:]
            token = tokensFloats[a]
            antennaIndex = antennaIndexes[a]
            if antennaIndex >= 0 and antennaIndex < HEIGHT:
                if token >= 0 and token <= 1 and dataColIndexes[antennaIndex]< \
                        WIDTH and dataColIndexes[antennaIndex] >= 0:
                    if mode == 0:
                        data[antennaIndex][dataColIndexes[antennaIndex]] = token
                        dataColIndexes[antennaIndex] += 1
                    elif mode == 1:
                        data[antennaIndex][dataColIndexes[antennaIndex]] = \
                            (data[antennaIndex][dataColIndexes[antennaIndex]] +
                             token) / 2.0
                        dataColIndexes[antennaIndex] -= 1



ani = animation.FuncAnimation(f, updateFrame, interval=REDRAW_INTERVAL)
if not TURN_OFF_PROJECTION:
    ani2 = animation.FuncAnimation(f2, updateFrame2, interval=REDRAW_INTERVAL)

#show windows
plt.show()



