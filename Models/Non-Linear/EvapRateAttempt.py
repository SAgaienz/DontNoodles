import numpy as np 
import matplotlib.pyplot as plt 
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d

ΔH_vap_ls =  [2500.9,2496.2,2491.4,2477.2,2467.7,2458.3,2453.5,2441.7,2429.8,32420.3,2406.0,2396.4,2381.9,2372.3,2357.7,2333.0,2308.0,2282.5,2266.9] # KJ/kg 
ΔH_vap_ls = [H*1000 for H in ΔH_vap_ls] # J/kg
T_vap_ls = [0.01,2,4, 10, 14,18, 20,25,30, 34, 40, 44,50, 54, 60, 70, 80, 90, 96]
T_vap_ls = [T + 273.15 for T in T_vap_ls]

ΔH_vap = interp1d(T_vap_ls, ΔH_vap_ls)

A_p_V = lambda V: 7.54717e-3*V # takes V in Litres and ouputs m2

def Logistic(x, L, x0, k):
    return (L)/(1 + np.exp(-k*(x-x0)))

def U(t):
    if t <1500:
        return 0
    if t >= 1500:
        return 3000 # Watt


def HSF(x, x_s):
    if x<x_s:
        return 0
    if x>=x_s:
        return 1

def R_evap(T , args): # We assume, for now, linear relation to Temperature and rate of evaporation.
    V, Ts, Tboil, h, T_evap_start = args
    σ = 5.67e-8
    r_evap_max = (3000 - A_p_V(V0)*h*(Tboil - Ts) - A_p_V(V0)*σ*(Tboil**4 - Ts**4))/(ΔH_vap(95+273.15)) 
    # define max evap rate for this volume
    # The volume will change, and hence, according to this relation, so too will the max. For now, we will say the volume change is neg..
    # We will base the MAX R_evap on the initial vol...
    if T<=T_evap_start:
        return 0
    elif T<=Tboil:
        m = (r_evap_max/(Tboil - T_evap_start)) 
        return m*(T-T_evap_start)
    else:
        return r_evap_max


def diff(t, arr):
    T, V, m_v = arr
    A = A_p_V(V0)
    Q = U(t)

    Ts = 25+273.15
    Cp = 4186 #J/kg.K
    
    h = 15
    σ = 5.67e-8 #W/m2.K4
    ρ_liq = 1 # for now... #kg/L 

    # λ =  ΔH_vap(T)
    λ =  2429.8 # J/kg
    Q_rad = σ*A*((T**4) - (Ts**4))
    Q_conv = h*A*(T - Ts)

    dm_vdt = R_evap(T, [V0, T0, 95+273.15, 15, 66+273.15]) 
    dVdt = -dm_vdt
    dTdt = (Q - Q_rad - Q_conv - dVdt*λ)/(Cp*V)
    return [dTdt, dVdt, dm_vdt]


tf = 20000
tspan = np.linspace(0, tf, 70000)

T0 = 273.15+25
V0 = 50
m_v = 0

Tans, Vans, m_v_ans = solve_ivp(diff, [0, tf], [T0, V0, m_v], dense_output=True).sol(tspan)

# fig, ax1 = plt.subplots()
# ax1.plot(tspan, [T-273.15 for T in ans1] )
# ax2 = plt.twinx()
# ax2.plot(tspan, [U(t) for t in tspan], alpha = 0.6,color = 'r')
# plt.show()


Tspan = np.linspace(25+273.15, 140+273.15, 300)

plt.plot(tspan, [a - 273.15 for a in Tans])
plt.show()
plt.plot(tspan, Vans)
plt.show()
plt.plot(tspan, m_v_ans)
plt.show()

