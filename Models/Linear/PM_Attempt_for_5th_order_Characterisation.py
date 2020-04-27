import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd 
import scipy.signal as sig 
from scipy.optimize import curve_fit 

df = pd.read_csv('70L_comp.csv', index_col= 'index')
xdata, ydata = df['time'], df['tem']
print(xdata)

def inp1(t):
    if t<33.358:
        return 0
    elif t>=33.358:
        return 3000

def resp(tspan, A, B, C, D, E, F, G, H):
    U = [inp1(t) for t in tspan]
    num = [A, A*B + A*C + A*D, A*B*C + A*B*D + A*C*D, A*B*C*D]
    den = [1, E + F + G + H, E*F + E*G + E*H + F*G + F*H + G*H, E*F*G + E*F*H + E*G*H + F*G*H, E*F*G*H]
    Gp = sig.lti(num, den)
    _, T, _ = sig.lsim(Gp, U, tspan)
    T = T + ydata[0]
    return T


tspan = np.linspace(0, 12000, 5000)
# plt.plot(tspan, resp(tspan, 1,1,1,1,1,1,1, 1))
# plt.show()

# B, _ = curve_fit(resp, xdata, ydata, full_output = 1)
# print(B)