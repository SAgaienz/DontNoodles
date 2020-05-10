import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation, writers


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

Uspan = np.linspace(0, 3000, 100)
Tspan = np.linspace(85+273.15, 273.15 + 100, 100)

Tspan, Uspan = np.meshgrid(Tspan, Uspan)
r_ev = R_evap(Tspan, 70, Uspan, [273.15+27, 96+273.15, 90+273.15, 15])


#plot 

norm = plt.Normalize(r_ev.min(), r_ev.max())
colors = cm.winter(norm(r_ev))
rcount, ccount, _ = colors.shape

fig = plt.figure()
ax = Axes3D(fig)

def init():
    ax.plot_wireframe(Tspan, Uspan, r_ev,  rcount=rcount*0.25, ccount=ccount*0.25, cmap=cm.winter)
    ax.set_xlabel('Liquid Temperature , °C')
    ax.set_ylabel('Element Input Power , W')
    ax.set_zlabel('Rate of Evaporation , kg/s')
    return fig,

def animate(i):
    ax.view_init(elev=30., azim=i)
    return fig,

# Animate
anim = FuncAnimation(fig, animate, init_func=init,
                               frames=360, interval=20, blit=True)
# Save
anim.save('Figures/Model Steps/Nonlinear Model/evap_func.mp4', fps=30, dpi = 500)