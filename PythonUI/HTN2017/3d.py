from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


def randrange(n, vmin, vmax):
    '''
    Helper function to make an array of random numbers having shape (n, )
    with each number distributed Uniform(vmin, vmax).
    '''
    return (vmax - vmin)*np.random.rand(n) + vmin

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

n = 100

xx = []
yy = []
zz = []

# For each set of style and range settings, plot n random points in the box
# defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
for zlow, zhigh in [(-50, -25), (-30, -5)]:
    xs = randrange(n, 23, 32)
    ys = randrange(n, 0, 100)
    zs = randrange(n, zlow, zhigh)
    ax.scatter(xs, ys, zs, cmap="autumn")
    xx.extend(xs)
    yy.extend(ys)
    zz.extend(zs)
from pprint import pprint
pprint(xx)
pprint(yy)
pprint(zz)
ax.plot_surface(xx, yy, zz,  rstride=4, cstride=4, cmap="blue")
plt.show()