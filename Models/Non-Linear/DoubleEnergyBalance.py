import numpy as np 
import matplotlib.pyplot as plt 
from scipy.integrate import solve_ivp

def Logistic(x, L, x0, k):
    return (L)/(1 + np.exp(-k*(x-x0)))

def U(t):
    if t <1500:
        return 0
    elif t >= 1500:
        return 3000 # Watt
    elif t>=12000:
        return 0
def HSF(x, x_s):
    if x<x_s:
        return 0
    if x>=x_s:
        return 1

def diff(t, T):
    Q = U(t)
    Ts = 25+273.15
    Cp = 4186 #J/kg.K
    V = 50 # l
    Ac = 0.2206 #m^2
    ht = 50e-3/Ac
    dia = 0.530 #m
    A = np.pi*dia*ht
    T_star = 66 + 273.15
    h = 15
    σ = 5.67e-8 #W/m2.K
    dmdt = 
    dTdt = (Q  - h*A*(T - Ts) - dmdt*λ*HSF(T, 95))/(Cp*V)
    return dTdt
tf = 20000
tspan = np.linspace(0, tf, 70000)
T0 = 273.15+25

ans1 = solve_ivp(diff, [0, tf], [T0], dense_output=True).sol(tspan)[0]

fig, ax1 = plt.subplots()
ax1.plot(tspan, [T-273.15 for T in ans1] )
ax2 = plt.twinx()
ax2.plot(tspan, [U(t) for t in tspan], alpha = 0.6,color = 'r')
plt.show()


Tspan = np.linspace(25, 110, 95-25+1)

