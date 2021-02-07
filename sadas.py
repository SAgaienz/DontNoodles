import matplotlib.pyplot as plt
import numpy as np
from numpy import ma
from matplotlib import ticker, cm

# N = 100
# x = np.linspace(-3.0, 3.0, N)
# y = np.linspace(-2.0, 2.0, N)

# X, Y = np.meshgrid(x, y)

# A low hump with a spike coming out.
# Needs to have z/colour axis on a log scale so we see both hump and spike.
# linear scale only shows the spike.
def HVS(T, Ts):
    return np.heaviside(T - Ts, 1)

ΔH_vap = lambda T: 2396.4e3 #J/kg
A_p_V = lambda V: 7.54717e-3*V 

def R_evap(T, V, U, args):
    Ts, Tboil, T_evap_start, h = args # all T in K
    σ = 5.67e-8
    A = 7.54717e-3*V
    r_evap_max = (3000 - A*h*(Tboil - Ts) - A*σ*(Tboil**4 - Ts**4))/ 2396.4e3
    κ = (1/3000)*U
    m = r_evap_max/(Tboil - T_evap_start)
    return (HVS(T, 0)*0 + HVS(T, T_evap_start)*(T - T_evap_start)*m + HVS(T, Tboil)*(r_evap_max - HVS(T, T_evap_start)*(T - T_evap_start)*m))*κ

Y = np.linspace(0, 3000, 100)
X = np.linspace(85+273.15, 273.15 + 100, 100)

X, Y = np.meshgrid(X, Y)
z = R_evap(X, 70,Y, [273.15+27, 96+273.15, 90+273.15, 15])
z = ma.masked_where(z <= 0, z)
fig, ax = plt.subplots()
cs = ax.contourf(X, Y, z, cmap=cm.PuBu_r)
cbar = fig.colorbar(cs)
plt.show()