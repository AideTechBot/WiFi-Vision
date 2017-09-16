#ay lmao

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib as mlp
import matplotlib.animation as animation

#hide the toolbar
mlp.rcParams['toolbar'] = 'None'

data = np.random.random(size=(4, 26))

#create a seperate window for the projector
fig = plt.figure()
sep = plt.imshow(data, interpolation='bicubic', aspect='auto')

#create a shared window for 4 diagrams
f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row')
ax1.imshow(data, interpolation='bicubic', aspect='auto', cmap='bone')
ax2.imshow(data, interpolation='bilinear', aspect='auto')
ax3.imshow(data, interpolation='kaiser', aspect='auto')
ax4.imshow(data, interpolation='sinc', aspect='auto')

def updateFrame(*args):
    global data
    data = np.random.random(size=(4,26))
    sep.set_array(data)
    return sep

ani = animation.FuncAnimation(fig, updateFrame, interval=50)
plt.show()

