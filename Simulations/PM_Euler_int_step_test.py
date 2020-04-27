import numpy as np 
import matplotlib.pyplot as plt 

def sys(V):
    K = (95-25)/3000
    τ , ζ =   (5.24404762*V) +  182.26190473,  (0.01010714*V) +  0.73178571
    return K, τ, ζ



def Euler_Sim_step(final_time,   dt,  Step_start_time , T_0, Vol):
    K, τ, ζ = sys(Vol)

    def U(t):
        if t<Step_start_time:
            return 0
        if t>= Step_start_time:
            return 3000


    N_tot = int(np.round(final_time/dt))
    nspan = range(N_tot)
    tspan = [t*dt for t in nspan]
    y = np.zeros(N_tot+1)
    x = np.zeros(N_tot+1)


    x[0] = T_0
    y[0] = 0
    for n in nspan:

        t = dt*n
        u = U(t)


        x[n+1] = x[n] + dt*y[n]
        y[n+1] = y[n] + dt*((1/(τ**2))*((K*u) - (x[n] - T_0) - (2*τ*ζ*y[n])))


    x = x[0:-1]
    y = y[0:-1]
    return [tspan, x]

plt.plot(*Euler_Sim_step(20000 , 2 , 4000, 26, 70))
plt.show()