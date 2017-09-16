
import matplotlib.pyplot as plt
from pprint import pprint
import numpy as np

data = np.random.random(size=(4, 26))
#data.fill(0)
"""
for i in range(15,25):
    for t in range(1,3):
        data[t][i]=1

for i in range(18,22):
    for t in range(0,4):
        data[t][i]=1
"""

for i in np.arange(0,1,0.05):
        data[int(i * 4)][int(i * 26)] = 1
        #if (1+ int(i * 4)) in range(0,4) and (1 + int(i * 26)) in range(0,26):
        #    data[1+ int(i * 4)][1 + int(i * 26)] = 1
        #if (-1+ int(i * 4)) in range(0,4) and (-1 + int(i * 26)) in range(0,
        # 26):
        #    data[-1+ int(i * 4)][-1 + int(i * 26)] = 1



pprint(data)

plt.imshow(data, interpolation='bicubic', aspect='auto', cmap='flag')
#plt.xticks(np.arange(0.0, 2.5, 1), np.arange(0.5, 2, 0.5))
#plt.yticks(np.arange(2, -0.5, -1), np.arange(0.5, 2, 0.5))

plt.show()