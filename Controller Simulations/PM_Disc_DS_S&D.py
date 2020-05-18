import numpy as np 
import matplotlib.pyplot as plt 

        # x[n+1] = x[n] + dt*y[n]
        # y[n+1] = y[n] + dt*((1/(τ**2))*((K*up) - (x[n] - T_0) - (2*τ*ζ*y[n]) + D(t)))

def sys(V):
    K = (95-25)/3000
    τ , ζ =   (5.24404762*V) +  182.26190473,  (0.01010714*V) +  0.73178571
    return K, τ, ζ

def DS_PID_Params(V, α):
    K, τ, ζ = sys(V)
    Kc, τ_I, τ_D = (2*ζ/(K*α)), 2*ζ*τ, τ/(ζ*2)
    return [Kc, τ_I, τ_D]


def D(t):
    if t<3000:
        return 0
    if t>= 3000:
        return -20

def Euler_Sim(tspan,   Tsp_span,  D_span , T_0, Vol):

    K, τ, ζ = sys(Vol)
    N_tot = len(tspan)
    nspan = range(N_tot)
    dt = tspan[1]

    T = np.zeros(N_tot+1)
    dTdt = np.zeros(N_tot+1)
    e = np.zeros(N_tot)
    u = np.zeros


tspan = np.linspace(0, 13, 14)
print(Euler_Sim(tspan, 3,2,1,2))

 