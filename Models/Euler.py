import numpy as np 
import matplotlib.pyplot as plt 

def Euler(func, tspan, y0, args):
    ylist = []
    y = y0
    ylist.append(y0)
    dt = tspan[1]
    tspan = tspan[:-1]
    for i, t in enumerate(tspan):
        yj_list = []
        for j, yj in enumerate(y):
            yj += func(t, yj, args)[j]*dt
            yj_list.append(yj)
        ylist.append(yj_list)
        y = yj_list
    ylist = np.array(ylist).T
    return ylist

def diff_func(t, y, args):
    dydt = y - t*y
    return [dydt, dydt*2]

tspan = np.linspace(0, 10, 110)
ys = Euler(diff_func, tspan, [1,0], 0)

plt.plot(tspan, ys[0])
plt.show()