import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D

ΔH_vap = lambda T: 2396.4e3 #J/kg
A_p_V = lambda V: 7.54717e-3*V 

def R_evap(T, V, U, args):
    Ts, Tboil, h, T_evap_start = args
    T, Ts, T_evap_start, Tboil = T + 273.15, Ts + 273.15, T_evap_start + 273.15, Tboil + 273.15
    σ = 5.67e-8
    r_evap_max = (3000 - A_p_V(V)*h*(Tboil - Ts) - A_p_V(V)*σ*(Tboil**4 - Ts**4))/ 2396.4e3
    mdpnt = (Tboil + T_evap_start)/2
    b = 0.7
    κ =  (1/3000)*U
    return (r_evap_max/(1 + np.exp(-b*(T - mdpnt))))*κ
# data 
Uspan = np.linspace(0, 3000, 100)
Tspan = np.linspace(25, 140, 100)
Tspan, Uspan = np.meshgrid(Tspan, Uspan)
r_ev = R_evap(Tspan , 50, Uspan ,  [27, 95, 15, 85])

# plots
fig = plt.figure(constrained_layout = True)
ax1 = fig.add_subplot(1,2,1,projection = '3d' )
surf = ax1.plot_wireframe(Tspan, Uspan, r_ev, rstride=5, cstride=5)
ax1.set_xlabel('Temperature, °C')
ax2 = fig.add_subplot(1,2,2)

cf = ax2.contourf(Tspan,r_ev, Uspan )
# ax2.set_xlim([85,95])
fig.colorbar(cf, ax=ax2, label = 'Element Power, kW')
# ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

plt.show()