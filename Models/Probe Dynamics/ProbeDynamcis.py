import pandas as pd 
import numpy as np 
import scipy.signal as sig 
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit

df = pd.read_csv('Probe Dynamics\ProbeData.csv')


xdata, ydata = df['time'].tolist(), df['dtemp'].tolist()
xdata = [int(x) for x in xdata]
def U(t):
    if t<196:
        return 0
    if t>=196:
        return 72


def resp(xdata, K, τ):
    res = []
    for x in xdata:
        if x<196:
            r = 0
        if x>=196:
            r = (K*(np.exp((x-196)/τ) - 1)*np.exp(-(x-196)/τ))*72
        res.append(r)
    return res

save_fig = str(input("save fig? (y/n)   "))

tspan = np.linspace(0, 500, 1000)
beta, resid = curve_fit(resp, xdata, ydata, p0 = [1, 16])
fig1 = plt.figure(1, figsize = (8,8))
plt.scatter(xdata, ydata, label = 'Probe Response (Tm(s)/T(s))')
plt.plot(tspan, resp(tspan, *beta), label = 'FO Model params: K = '+ str(np.round(beta[0], 3)) + ' , τ = '+ str(np.round(beta[1], 3)), color = 'r')
plt.plot(tspan, [U(x) for x in tspan], color = 'm', label = 'Probe Unit Step (T(s) = 72/s)')
plt.legend(loc = 'upper left')
plt.xlabel('Time \n seconds')
plt.ylabel('Temperature \n $^\circ C$')
plt.grid(True)
plt.axis([-13,426,-2.6,90])
if save_fig=='y':
    plt.savefig('Figures\ProbeDynamicsPlot.png', dpi = 200)
    plt.show()
else:
    plt.show()