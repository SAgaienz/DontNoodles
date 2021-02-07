import numpy as np 
import matplotlib.pyplot as plt 
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d
import pandas
from scipy.signal import square
from dataconfig import datadir

df = pandas.read_csv(datadir / r'Cleaned_70L/Cleaned_70L_Step_data.csv')
xdata, ydata = df['time'].tolist(), df['tem'].tolist()

def HVS(T, Ts):
    return np.heaviside(T - Ts, 1)

def NonLinearModel(tspan, U_Func, sys_args): #### Takes in a tspan, a U function such that U = f(t) and parameters
    T0, V0, m_v0, Ts, Tboil, T_ev_s, h = sys_args
    U = lambda t:  U_Func(t)
    

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

    init_cond = [T0, V0, m_v0]
    args = [Ts, Tboil, T_ev_s, h]
    ans = solve_ivp(lambda t, arr: nonlinear_mod(t, arr, args), [0, tf] , init_cond , dense_output=True).sol(tspan)
    ar = list(map(list, zip(*ans)))
    Uspan = [U(t) for t in tspan]
    b = [nonlinear_mod(tspan[i], ar[i], args) for i in range(len(tspan))]
    b = list(map(list, zip(*b)))
    return [tspan, ans , Uspan, b]

def U(t): 
    if t<=33:
        return 0
    if t>33 and t<=15000:
        return 3000
    if t>15000:
        return 0

def U1(t): 
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

def U2(t): # Pulse
    return ((square(t, 0.5)+1)/2)*3000

def sus_step(t):
    if t<0.5*3600:
        return 0.1
    if t>=0.5*3600:
        return 3000

Ts = 27 # °C (Surrounds Temperature)
T0 = Ts # °C (Initial temp of liquid, we assume the surrounds temperature does not change)
V0 = 60 # L (initial Voume in L)
m_v0 = 0 # kg (initial mass of water in vapour phase)
h = 15 # W/m2.K (Assumption for now... )
Tboil = 95 # °C (classical boiling point at the system P)
T_ev_s = 90 # °C (temperature we expect to start having evaporation (nucleate boiling))

tf = 3600*12
tspan = np.linspace(0, tf, 100000)
argus = [T0, V0, m_v0, Ts, Tboil, T_ev_s, h]
_, ans, Uspan, diffs = NonLinearModel(tspan, U1, argus)

plt.subplot(5,1,1)
plt.ylabel('Temperature, °C')
plt.plot(tspan/3600, ans[0], label = 'Model: 70L')
plt.scatter([x/3600 for x in xdata], ydata, color = 'r', label = 'Step Test data: 70L')
plt.legend(loc= 'best')
plt.subplot(5,1,2)
plt.plot(tspan/3600, ans[1])
plt.ylabel('Liquid Volume, L')
plt.subplot(5,1,3)
plt.plot(tspan/3600, ans[2])
plt.ylabel('Mass Evaporated, kg')
plt.subplot(5,1,4)
plt.plot(tspan/3600, Uspan)
plt.ylabel('Element Input Power, W')
plt.subplot(5,1,5)
plt.plot(tspan/3600, diffs[2])
plt.ylabel(r'$r_{e}$, kg/s')
plt.xlabel('time, hours')
plt.show()
