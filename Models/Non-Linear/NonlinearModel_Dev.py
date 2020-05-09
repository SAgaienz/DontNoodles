import numpy as np 
import matplotlib.pyplot as plt 
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d
import pandas

df = pandas.read_csv('Data/Cleaned_70L_Step_data.csv')
xdata, ydata = df['time'].tolist(), df['tem'].tolist()


def NonLinearModel(tspan, U_Func, sys_args): #### Takes in a tspan, a U function such that U = f(t) and parameters
    T0, V0, m_v0, Ts, Tboil, T_ev_s, h = sys_args
    U = lambda t:  U_Func(t)
    def R_evap(T, V, U, args):
        Ts, Tboil, T_evap_start, h = args # all T in K
        σ = 5.67e-8
        A = 7.54717e-3*V
        r_evap_max = (3000 - A*h*(Tboil - Ts) - A*σ*(Tboil**4 - Ts**4))/ 2396.4e3
        mdpnt = (Tboil + T_evap_start)/2
        b = 0.9 
        κ = (1/3000) *U
        return (r_evap_max*κ)/(1 + np.exp(-b*(T - mdpnt))) # kg H2O/s (Logistic Curve)

    def nonlinear_mod(t, arr, args): 
        T, V, _ = arr #  All T input as °C
        Ts, Tboil, T_evap_start, h = args
        T, Ts, Tboil, T_evap_start = T + 273.15,  Ts + 273.15, Tboil + 273.15, T_evap_start + 273.15
        
        Q = U(t)
        A = 7.54717e-3*V
        Cp = 4186 #J/kg.K
        λ =  2396.4e3
        σ = 5.67e-8

        dm_vdt = R_evap(T, V, Q, [Ts, Tboil, T_evap_start, h]) 
        dVdt = -dm_vdt
        dTdt = (Q - (h*A*(T - Ts)) - (σ*A*((T**4) - (Ts**4))) - dm_vdt*λ)/(Cp*V)
        return [dTdt, dVdt, dm_vdt]

    init_cond = [T0, V0, m_v0]
    args = [Ts, Tboil, T_ev_s, h]
    ans = solve_ivp(lambda t, arr: nonlinear_mod(t, arr, args), [0, tf] , init_cond , dense_output=True).sol(tspan)
    Uspan = [U(t) for t in tspan]
    return [tspan, ans , Uspan]

def U1(t):
    if t>=0 and t<33:
        return 0
    if t>=33 and t<5000:
        return 3000
    else:
        return 3000


Ts = 27 # °C (Surrounds Temperature)
T0 = Ts # °C (Initial temp of liquid, we assume the surrounds temperature does not change)
V0 = 70 # L (initial Voume in L)
m_v0 = 0 # kg (initial mass of water in vapour phase)
h = 15 # W/m2.K (Assumption for now... )
Tboil = 95 # °C (classical boiling point at the system P)
T_ev_s = 85 # °C (temperature we expect to start having evaporation (nucleate boiling))

tf = 3600*6
tspan = np.linspace(0, tf, 10000)
argus = [T0, V0, m_v0, Ts, Tboil, T_ev_s, h]
_, ans, Uspan = NonLinearModel(tspan, U1, argus)

plt.subplot(2,1,1)
plt.plot(tspan/3600, ans[0])
plt.scatter([x/3600 for x in xdata], ydata, color = 'r')
plt.subplot(2,1,2)
plt.plot(tspan/3600, Uspan)
plt.show()
