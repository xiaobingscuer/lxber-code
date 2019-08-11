from mpl_toolkits.mplot3d import Axes3D

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import math

def nonlinear(k, sign = 'sin'):
    if sign == 'sin':
        return math.sin(k)
    elif sign == 'cos':
        return math.cos(k)
    else:
        return math.tan(k)

point = [[4,9,2],[3,5,7],[8,1,6],[4,3,8],[9,5,1],[2,7,6],[4,5,6],[2,5,8]]
points = []
sums = []
maxk = 2*math.pi
maxk = 10
num = 20.0
print(maxk/num)
#ks = [k for k in range(maxk)]
#ks = [k for k in np.arange(-maxk, maxk, maxk/num)]
ks = [k for k in np.arange(-maxk, maxk, maxk/num)]
#ks = [k for k in np.arange(0.001, maxk, maxk/num)]

for k in ks:
    t = []
    ss = []
    for p in point:
        tt = [0, 0, 0]
        s = 0
        for j in range(3):
            #tt[j] = p[j] + p[(j + 1) % 3]
            #tt[j] = p[j] * k + p[(j + 1) % 3]*k/10
            #tt[j] = p[j] * nonlinear(k,'sin') + p[(j + 1) % 3]*1
            #tt[j] = p[j] * nonlinear(k,'sin') + p[(j + 1) % 3]*nonlinear(k,'cos')
            #tt[j] = p[j] * nonlinear(k,'sin') + p[(j + 1) % 3] * nonlinear(k,'cos') + p[(j + 2) % 3]*nonlinear(k,'tan')
            #tt[j] = p[j] * nonlinear(k,'sin') + p[(j + 1) % 3] * nonlinear(k,'cos') + p[(j + 2) % 3]*0.1
            #tt[j] = p[j] * nonlinear(k,'sin') + p[(j + 1) % 3] * 1 + p[(j + 2) % 3] * 1
            #tt[j] = p[j] * k + p[(j + 1) % 3] * k/10 + p[(j + 2) % 3]*k/100
            #tt[j] = p[j] * 1+ p[(j + 1) % 3] * 1 + p[(j + 2) % 3]*1
            s += tt[j]
        t.append(tt)
        ss.append(s)
    points.append(t)
    sums.append(ss)

for ki in range(len(ks)):
    print(points[ki])
    print(sums[ki])
    print(sums[ki][0]/15)



plt.rcParams['legend.fontsize'] = 1

fig = plt.figure()
ax = fig.gca(projection='3d')

for point in points:
    for ex, ey, ez, c, m, la in [(point[i][0], point[i][1], point[i][2], 'r', 'o', i) for i in range(8)]:
        ax.scatter(ex, ey, ez, c=c, marker=m, s=1)
        #ax.text(ex, ey, ez, la, color='red')

    for i in range(8):
        for j in range(i, 8):
            ax.plot([point[i][0], point[j][0]], [point[i][1], point[j][1]], [point[i][2], point[j][2]], label='luoshu 3d', linewidth=1.0, color='black')
            pass

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

#ax.view_init(elev=20, azim=30)

plt.show()
