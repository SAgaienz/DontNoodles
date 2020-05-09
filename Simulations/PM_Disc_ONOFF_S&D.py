import numpy as np 
import matplotlib.pyplot as plt 

def sys(V):
    K = (95-25)/3000
    τ , ζ =   (5.24404762*V) +  182.26190473,  (0.01010714*V) +  0.73178571
    return K, τ, ζ

def Euler_ON_OFF(final_time,   dt, Tsp,  dist_start_time , T_0, Vol):

    K, τ, ζ = sys(Vol)

    def D(t):
        if t<dist_start_time:
            return 0
        if t>= dist_start_time:
            return -20


    N_tot = int(np.round(final_time/dt))
    nspan = range(N_tot)
    tspan = [t*dt for t in nspan]
    y = np.zeros(N_tot+1)
    x = np.zeros(N_tot+1)
    e = np.zeros(N_tot)
    u = np.zeros(N_tot)

    x[0] = T_0
    y[0] = 0

    for n in nspan:
        ep = np.round(Tsp - x[n], 2)
        ep = Tsp - x[n]
        t = dt*n
        
        if ep>0:
            up = 3000
        if ep<=0:
            up = 0

        x[n+1] = x[n] + dt*y[n]
        y[n+1] = y[n] + dt*((1/(τ**2))*((K*up) - (x[n] - T_0) - (2*τ*ζ*y[n]) + D(t)))

        e[n] = ep
        u[n] = up


    x = x[0:-1]
    y = y[0:-1]
    return [tspan, x, e, u]


tspan, x, e, u = Euler_ON_OFF(20000 , 2 ,85 , 10000, 26, 70)

plt.subplot(3, 1, 1)
plt.plot(tspan, x)
plt.subplot(3, 1, 2)
plt.plot(tspan, e)
plt.subplot(3, 1, 3)
plt.plot(tspan, u, linewidth = 0.5, alpha = 1, color = 'black')
plt.show()