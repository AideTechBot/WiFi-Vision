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

from matplotlib.widgets import Button


class Callback(object):

    def onStartPressed(self, event):
        print 'start pressed'
        global serialRW
        serialRW.write("G".encode())

    def onBasePressed(self, event):
        print 'base pressed'



#constants
WIDTH = 100 #(num increments on track)
HEIGHT= 6 #(num antennas)
REDRAW_INTERVAL = 100
OUTER_INPUT_RANGE = [10.0,80.0]
INPUT_RANGE = [30.0,60.0]
DEPTH_IN_Z = True #If false, depth in Y
ONLY_DRAW_3D_ON_COMPLETE = True
ONLY_DRAW_PROJECTION_ON_COMPLETE = False

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

data = np.zeros((HEIGHT,WIDTH))
#I think it uses the initial range in data points as a the permanent range
#needs the '1' to get the full scale
data[0][0] = float(1)


#Keeps track of which coloumn to write to for each antenna
dataColIndexes = [0]*HEIGHT

#0 -> baseline1
#   visible: goes to right, getting blurry data and drawing it as such
#   invisible: store in data
#1 -> baseline2
#   visible: goes to left, data appears hardly blurry
#   invisible: filter and avg into data
#2 -> detect1
#3 -> detect2
mode = 0


#hide the toolbar
mlp.rcParams['toolbar'] = 'None'

#for 3D map, turns 2D data array (x,y)->z into three 1D parallel arrays
def dataToXYZarrays():
    X = []
    Y = []
    Z = []
    for i in range(0,HEIGHT):
        for t in range(0, WIDTH):
            X.append(t)
            Y.append(i)
            Z.append(data[i][t])
    if DEPTH_IN_Z:
        return X, Y, Z
    else:
        return X, Z, Y


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
axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Start Reading')
bnext.on_clicked(callback.onStartPressed)
bprev = Button(axprev, 'Previous')
#bprev.on_clicked(callback.prev)


#create projection window
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
ax4.set_axis_off()

#initial renders
sem1 = ax1.imshow(data, interpolation='nearest', aspect=scaleReq,
                  extent=[0, WIDTH, 0, HEIGHT], cmap='bone')

X,Y,Z = dataToXYZarrays()
ax2.plot_trisurf(X,Y,Z, cmap="hot", shade="true")

sem3 = ax3.imshow(data, aspect=scaleSq, interpolation='bilinear',
                  extent=[0, WIDTH, 0, HEIGHT], cmap='plasma')

sem4 = ax4.imshow(data, interpolation='bilinear', aspect='auto',
                  extent=[0, WIDTH, 0, HEIGHT], cmap='binary')



def updateFrame(*args):
    global data
    global sem1
    global sem3
    global sem4
    #pprint(data)
    readSerial()
    sem1.set_array(data)
    if not ONLY_DRAW_3D_ON_COMPLETE:
        X, Y, Z = dataToXYZarrays()
        ax2.plot_trisurf(X, Y, Z, cmap="hot",shade="true")
    sem3.set_array(data)
    if not ONLY_DRAW_PROJECTION_ON_COMPLETE:
        sem4.set_array(data)

def updateFrame2(*args):
    if not ONLY_DRAW_PROJECTION_ON_COMPLETE:
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
    global dataColIndex
    global dataRowIndex
    global data
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
                fl = float(m(fl))
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
            token = tokensFloats[a]
            antennaIndex = antennaIndexes[a]
            if antennaIndex >= 0 and antennaIndex < HEIGHT:
                if fl >= 0 and fl <= 1:
                    data[antennaIndex][dataColIndexes[antennaIndex]] = token
                dataColIndexes[antennaIndex] += 1
                if dataColIndexes[antennaIndex] >= WIDTH:
                    dataColIndexes[antennaIndex] = 0
                serialString = serialString[serialString.find(",")+1:]


ani = animation.FuncAnimation(f, updateFrame, interval=REDRAW_INTERVAL)
ani2 = animation.FuncAnimation(f2, updateFrame2, interval=REDRAW_INTERVAL)

#show windows
plt.show()



