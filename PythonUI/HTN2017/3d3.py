from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
X, Y, Z = axes3d.get_test_data(0.05)
s = ax.plot_trisurf([0,1,2,0,1,2], [0,0,0,1,1,1], [1,0,2,1,0,2], cmap="hot",
                shade="true")
s.set_array


from pprint import pprint
pprint(Y)
plt.show()

