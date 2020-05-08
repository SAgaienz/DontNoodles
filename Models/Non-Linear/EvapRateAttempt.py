import numpy as np 
import matplotlib.pyplot as plt 
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d
import pandas

df = pandas.read_csv('Data\Cleaned_70L_Step_data.csv')

ΔH_vap = lambda T: 2396.4e3 #J/kg  (keeping this like this so we can complicate later)
A_p_V = lambda V: 7.54717e-3*V # takes V in Litres and ouputs m2
t_on = 33

def Logistic(x, L, x0, k):
    return (L)/(1 + np.exp(-k*(x-x0)))

def U1(t):
    if t>=0 and t<33:
        return 0
    if t>=33 and t<5000:
        return 3000
    if t>=5000 and t<20000:
        return 0
    else:
        return 0

def U(t):
    if t<=t_on:
        return 0
    if t> t_on:
        return 3000

def QConv(V, T, Ts):
    h = 15
    return h*A_p_V(V)*(T - Ts)

def QRad(V, T, Ts):
    σ = 5.67e-8
    return σ*A_p_V(V)*((T**4) - (Ts**4))

def HSF(x, x_s):
    if x<x_s:
        return 0
    if x>=x_s:
        return 1

def R_evap(T , V, U , args): # We assume, for now, linear relation to Temperature and rate of evaporation.
    Ts, Tboil, h, T_evap_start = args
    σ = 5.67e-8
    r_evap_max = (3000 - A_p_V(V)*h*(Tboil - Ts) - A_p_V(V)*σ*(Tboil**4 - Ts**4))/ 2396.4e3 
    # define max evap rate for this volume
    # The volume will change, and hence, according to this relation, so too will the max. For now, we will say the volume change is neg..
    # We will base the MAX R_evap on the initial vol...
    κ = lambda U: (1/3000)*U
    if T<=T_evap_start:
        return 0*κ(U)
    elif T<=Tboil:
        m = (r_evap_max/(Tboil - T_evap_start)) 
        return m*(T-T_evap_start)*κ(U)
    else:
        return r_evap_max*κ(U)

def R_evap2(T, V, U, args):
    Ts, Tboil, h, T_evap_start = args
    σ = 5.67e-8
    r_evap_max = (3000 - A_p_V(V)*h*(Tboil - Ts) - A_p_V(V)*σ*(Tboil**4 - Ts**4))/ 2396.4e3
    mdpnt = (Tboil + T_evap_start)/2
    b = 0.9
    κ = lambda U: (1/3000) *U
    return r_evap_max/(1 + np.exp(-b*(T - mdpnt)))*κ(U)


def diff(t, arr):
    T, V, m_v = arr
    Q = U1(t)
    Cp = 4186 #J/kg.K
    λ =  ΔH_vap(T)
    dm_vdt = R_evap2(T, V, Q, [Ts, 95+273.15, 15, T_star]) 
    dVdt = -dm_vdt
    dTdt = (Q - QConv(V, T, Ts) - QRad(V, T, Ts) - dm_vdt*λ)/(Cp*V)
    return [dTdt, dVdt, dm_vdt]

T_star = (90 + 273.15)
tf = 50000
tspan = np.linspace(0, tf, 100000)
T0 = 273.15 + 26.875
V0 = 70
m_v = 0
Ts = T0

Tans, Vans, m_v_ans = solve_ivp(diff, [0, tf], [T0, V0, m_v], dense_output=True).sol(tspan)
ansTrans = list(map(list, zip(*[Tans, Vans, m_v_ans])))



plt.subplot(3,1,1)
plt.plot(tspan/3600, [T - 273.15 for T in Tans], label = 'Model: 70L')
plt.plot(df['time']/3600, df['tem'], color = 'red', label = 'Data: 70L')
plt.legend(loc = 'best')
plt.subplot(3,1,2)
plt.plot(tspan/3600, Vans )
plt.subplot(3,1,3)
plt.plot(tspan/3600, m_v_ans )
plt.show()