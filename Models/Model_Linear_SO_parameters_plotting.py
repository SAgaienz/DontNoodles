
# %%
import numpy as np 
import os
from scipy.optimize import curve_fit
import scipy.signal as sig 
import matplotlib.pyplot as plt 
from ipywidgets import interact
from dataconfig import datadir

# %%
def time_to_boil(Tf, V):
    Cp = 4.186
    t = (Cp*V*(Tf - 22)*1000*1.1)/3000
    return t
Vspan = [30,40,50,60,70,80,90,100]
Tlist = [time_to_boil(95, V) for V in Vspan]


# %%
tf = 12000
tspan = np.linspace(0, tf, ((tf+1)*10) )


# %%
def Q_in(t):
    if t<0:
        return 0
    if t>=0:
        return 3000


# %%
def Resp(tspan, τ, ζ):
    K = (95-22)/3000
    U = [Q_in(t) for t in tspan]
    Gp = sig.lti([K], [τ, 2*ζ*τ, 1])
    _, T, _ = sig.lsim(Gp, U, tspan)
    T = T + 22
    return T


# %%
parms = np.array([[330, 1], 
         [390, 1.08], 
         [440, 1.28], 
         [520, 1.39], 
         [570, 1.47], 
         [590, 1.57], 
         [625, 1.65], 
         [720, 1.67]])


# %%
def Linear_approx(V, m, c):
    return m*V + c


# %%
beta1, _ = curve_fit(Linear_approx,Vspan,  parms.T[0], p0 = [50,1])
beta2, _ = curve_fit(Linear_approx,Vspan,  parms.T[1], p0 = [50,1])

# %%

my_path1 =  datadir
my_file1 = r'Figures/Linear_parameters.png'

# %%
fig1, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
fig1.set_figheight(6)
fig1.set_figheight(5)
ax1.plot(Vspan, [Linear_approx(V, *beta1) for V in Vspan], color = 'r', label = str(np.round(beta1[0], 3) )+'V'+' + ' + str(np.round(beta1[1], 3)))
ax1.scatter(Vspan, parms.T[0], label = 'τ for SO Model')
ax1.set(ylabel='τ \n seconds')
ax1.legend(loc = 'best')

ax2.plot(Vspan, [Linear_approx(V, *beta2) for V in Vspan], color = 'r', label = str(np.round(beta2[0], 3) )+'V'+' + ' + str(np.round(beta2[1], 3)))
ax2.scatter(Vspan, parms.T[1], label = 'ζ for SO Model')
ax2.set(xlabel='Volume \n Litres', ylabel='ζ ')
ax2.legend(loc = 'best')

fig1.tight_layout()
fig1.savefig(datadir / my_file1, dpi = 300)
fig1.show()

my_file2 = r'Figures/LinearParmsResponse.png'


# %%
fig3, ax =  plt.subplots(1,1)
fig3.set_figheight(6)
fig3.set_figwidth(8)
for V in Vspan:
    ax.scatter(time_to_boil(95, V), 95)
    ax.plot(tspan, Resp(tspan, Linear_approx(V, *beta1), Linear_approx(V, *beta2)), label =str(V) + ' Litres')
ax.legend(loc = 4)
ax.set_xlabel('Time \n Seconds')
ax.set_ylabel('Temperature \n $^\circ$C')
fig3.savefig(datadir / my_file2, dpi = 300)
fig3.show()

# %%



# %%



# %%



