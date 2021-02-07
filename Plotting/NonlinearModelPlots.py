import matplotlib.pyplot as plt 
from matplotlib import rc
import numpy as np 

rc("text", usetex=True)
rc("font", family="serif")
datadir = '/run/media/sagaienz/Internal/UserData/Documents/ChemEng/CSC/Poster'
rep_repo_dir = "/home/sagaienz/ChemEng/CSC/CSC411 Report Repo/Figures/Results"

def Euler(func, tspan, y0, args):
    ylist = []
    y = y0
    ylist.append(y0)
    dt = tspan[1]
    tspan = tspan[:-1]
    for i, t in enumerate(tspan):
        yj_list = []
        for j, yj in enumerate(y):
            yj += func(t, y, args)[j]*dt
            yj_list.append(yj)
        ylist.append(yj_list)
        y = yj_list
    ylist = np.array(ylist).T
    return ylist

def HVS(T, Ts):
    return np.heaviside(T - Ts, 1)

def R_evap(T, V, U, args):
        Ts, Tboil, T_evap_start, h = args # all T in K
        σ = 5.67e-8
        A = 7.54717e-3*V
        r_evap_max = (3000 - A*h*(Tboil - Ts) - A*σ*(Tboil**4 - Ts**4))/ 2396.4e3
        κ = (1/3000)*U
        m = r_evap_max/(Tboil - T_evap_start)
        return (HVS(T, 0)*0 + HVS(T, T_evap_start)*(T - T_evap_start)*m + HVS(T, Tboil)*(r_evap_max - HVS(T, T_evap_start)*(T - T_evap_start)*m))*κ, r_evap_max

def nonlinear_mod(t, arr, args): 
    T, V, _ = arr #  All T input as °C
    Ts, Tboil, T_evap_start, h = args
    T, Ts, Tboil, T_evap_start = T + 273.15,  Ts + 273.15, Tboil + 273.15, T_evap_start + 273.15
    
    Q = U(t)
    A = 7.54717e-3*V
    Cp = 4186 #J/kg.K 
    λ =  2396.4e3
    σ = 5.67e-8
    r_evap_max = R_evap(T, V, Q, [Ts, Tboil, T_evap_start, h])[1]
    dm_vdt = R_evap(T, V, Q, [Ts, Tboil, T_evap_start, h])[0]
    dVdt = -dm_vdt
    rad = (σ*A*((T**4) - (Ts**4)))
    # rad =0
    dTdt = (Q - (h*A*(T - Ts)) - rad - dm_vdt*λ)/(Cp*V)
    if abs(r_evap_max -  dm_vdt) < 0.00001:
        if abs(T -  Tboil) < 0.1:
            dTdt = 0
    return [dTdt, dVdt, dm_vdt]

def U(t): 
    if t<=33:
        return 0
    if t>33 and t<=3600*2.5:
        return 3000
    if t>3600*2.5 and t<=4.5*3600:
        return 0    
    if t>4.5*3600 and t<=8*3600:
        return 1500
    if t>8*3600:
        return 0

Ts = 27 # °C (Surrounds Temperature)
T0 = Ts # °C (Initial temp of liquid, we assume the surrounds temperature does not change)
V0 = 80 # L (initial Voume in L)
m_v0 = 0 # kg (initial mass of water in vapour phase)
h = 15 # W/m2.K (Assumption for now... )
Tboil = 95 # °C (classical boiling point at the system P)
T_ev_s = 90 # °C (temperature we expect to start having evaporation (nucleate boiling))

tf = 3600*12
tspan = np.linspace(0, tf, 10000)
y0 = [T0, V0, m_v0] 
argus = [Ts, Tboil, T_ev_s, h]
Tspan, Vspan, mspan = Euler(nonlinear_mod, tspan, y0, args = argus)
Qspan = [U(t) for t in tspan]
save = True
aspect_ratio = 4 / 5
FULLSIZE = 4.5, 4.5 * aspect_ratio
HALFSIZE = 3, 3 * aspect_ratio
ts = [t/3600 for t in tspan]
Pcol = '#0101ff'
Tcol = '#391d52'
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=FULLSIZE)
ax1b = ax1.twinx()
ax1.plot(ts, Tspan, color = Tcol, label = str(V0) + ' L')
ax1.set_ylabel(r'Temperature'+"\n"+ "$^\circ C$")
ax1.set_ylim(0, 105)
ax1.legend(loc = 'lower right')
ax1b.plot(ts, Qspan, color = Pcol)
ax1b.set_ylabel(r'Element Power'+"\n"+ "$kW$", color = Pcol)
ax1b.tick_params(which='major', color = Pcol, labelcolor = Pcol)
ax1b.set_ylim(-5, 4000)
ax1.grid()

ax2.plot(ts, Vspan, color = Pcol)
ax2.set_ylabel(r'Liquid Volume'+"\n"+ "$L$")
ax2.grid()

ax2.set_xlabel(r'Time' + "\n" + 'h')
ax2.set_xlim(0, 11)
plt.tight_layout()
fig.align_ylabels()
if save:
    plt.savefig(rep_repo_dir+"/"+'liquidLev2.pdf')
plt.show()
