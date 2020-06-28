import numpy as np 
import matplotlib.pyplot as plt 

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
    T, V, Q  = arr #  All T input as °C
    Ts, Tboil, T_evap_start, h = args
    T, Ts, Tboil, T_evap_start = T + 273.15,  Ts + 273.15, Tboil + 273.15, T_evap_start + 273.15
    
    A = 7.54717e-3*V
    Cp = 4186 #J/kg.K 
    λ =  2396.4e3
    σ = 5.67e-8
    dm_vdt, r_evap_max = R_evap(T, V, Q, [Ts, Tboil, T_evap_start, h])
    dVdt = -dm_vdt
    rad = (σ*A*((T**4) - (Ts**4)))
    # rad =0
    dTdt = (Q - (h*A*(T - Ts)) - rad - dm_vdt*λ)/(Cp*V)
    if abs(r_evap_max -  dm_vdt) < 0.00001:
        if abs(T -  Tboil) < 0.1:
            dTdt = 0
    return [dTdt, dVdt]

Ts = 27 # °C (Surrounds Temperature)
T0 = Ts # °C (Initial temp of liquid, we assume the surrounds temperature does not change)
V0 = 70 # L (initial Voume in L)
m_v0 = 0 # kg (initial mass of water in vapour phase)
h = 15 # W/m2.K (Assumption for now... )
Tboil = 95 # °C (classical boiling point at the system P)
T_ev_s = 90 # °C (temperature we expect to start having evaporation (nucleate boiling))

argus = [Ts, Tboil, T_ev_s, h]

ts = np.linspace(0, 5*3600, 100)
dt = ts[1]

Tsp = 85
def Tsp_f(t):
    if t<3*3600:
        return 85
    if t>3*3600:
        return 75

Q = np.zeros_like(ts)
T = np.zeros_like(ts)
V = np.zeros_like(ts)
e = np.zeros_like(ts)
T[0] = T[1] = T[2] = T0
V[0] = V[1] = V[2] = V0

Kc, tI, tD = 50, 10, 60

for i in range(2, len(ts)):
    dTdt, dVdt = nonlinear_mod(dt, [T[i-1], V[i-1], Q[i-1]], argus)
    T[i] = T[i-1] + dTdt*dt
    V[i] = V[i-1] + dVdt*dt
    e[i] = Tsp_f(ts[i]) - T[i]

    Q[i] = Kc*(1 + (dt/tI)*(e[i]) + (tD/dt)*(e[i]- 2*e[i-1] + e[i-2]) )
    if Q[i] > 3000:
        Q[i] = 3000
    if Q[i]<0:
        Q[i] = 0


tplot = [t/3600 for t  in ts]
fig, (ax1, ax2, ax3) = plt.subplots(3,1, sharex = True)
ax1.plot(tplot, T)
ax1.plot(tplot, [Tsp_f(t) for t in ts])
ax2.plot(tplot, Q)
ax3.plot(tplot, V)
plt.show()