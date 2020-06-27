import numpy as np 
import pandas 
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit, fsolve
from scipy.signal import lti, lsim
from scipy.interpolate import interp1d
from dataconfig import datadir
from matplotlib import cm, rc

df_Aux = pandas.read_csv(datadir / 'Cleaned_70L/Cleaned_70L_Step_data.csv')
# 70L step test data

xdata, ydata = df_Aux['time'].tolist(), df_Aux['tem'].tolist()
xdata1, ydata1 = xdata[0:1400], ydata[0:1400]


# initial/on values 
i_on = 7
t_on = xdata[i_on]
T0 = np.mean(ydata[0:5])

# The Values where T_final = 92C
i_f = 1397 #index
t_f = xdata[i_f]
T_f = ydata[i_f]

print(t_on, T0,t_f , T_f)

tspan = np.linspace(0, 11000, 20000)

# Time that we turned the element on at (unit step)
def U(t):
    if t<t_on:
        return 0
    if t>=t_on:
        return 3000

def U1(t):
    if t<t_on:
        return 0
    if t>=t_on and t<5000:
        return 3000
    else:
        return 0
        

# First order Model
def fo(tspan, K, τ , U  = U):
    Uspan = [U(t) for t in tspan]
    Gp = lti(K, [τ , 1 ])
    _, Tl, _ = lsim(Gp, Uspan, tspan)
    Tl = Tl + T0
    return Tl


# Regression
B70, res =  curve_fit(fo, xdata1, ydata1, [100000, 5000])

# Because of the COVID-19 Pandemic, it is impossible to find the actual dependence of the system parameters (physical properties) so we will infer them as follows...
# Assume that the factor by which the time to boil is extended by over ideality is constant for all volumes...
# We will call this factor κ = (Time it actually took to get to 95C) / (time it theoretically should take to get to 95C) (s/s)
t_t_b_70 = 4.186*70*(T_f - T0)/3 #Theoritcal time taken to get to 92C from 27C for 70L (Cp calc: P = 3kW, Cp = 4.186)
κ = ((t_f - t_on)/t_t_b_70)
# print(κ)
def time_to_boil(V, κ):
    return (4.186*V*(T_f - T0)/3)*κ 

# We will assume that the gain of the system has no dependance on volume (the gain of the FO linear model is constant)
def K_and_τ( tf, Tf): 
    K = B70[0] # constant K (from bit)
    τ = -tf/(np.log(1 - ((Tf - T0)/(K*3000))))# Time domain response of FO, solved for τ 
    return [K,τ]

Vspan = np.arange(30, 100, 10)
parms = {}
for V in Vspan:
    t_end = time_to_boil(V, κ)
    K, τ  = K_and_τ(t_end, 92)
    parms['V' + str(V)] = K, τ
# This (above) becomes unnecessary if we just sub "time_to_boil" into "K_and_τ" and sub 1 for "V" in "time_to_boil"
# # Bringing the dependence together...
def Params(V):
    K, τ = 0.06519652149867068 , 265.02732767188155*V
    return K, τ 


rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

# (0.267004, 0.004874, 0.329415, 1.0)
save_figs = False
Vspan = [30, 40,50,60,70,80,90]
cols2 = [cm.viridis(i) for i in np.linspace(0, 1, len(Vspan)+1)]
tspan2 = np.linspace(0, 5*3600, 1000)
fig2, ax1 = plt.subplots(1,1, sharex = True ,figsize=[4,16/5])
ax1.plot([x/3600 for x in xdata], ydata, color = 'k', label = 'Exp.')
for i in range(0, len(Vspan)):
    ax1.plot([t/3600 for t in tspan2], fo(tspan2, *Params(Vspan[i])) ,  color = cols2[i+1], label = str(Vspan[i])+' L')
    ax1.plot([time_to_boil(Vspan[i], κ)/3600], [T_f],  color = cols2[i+1], ls = '', marker = 'o', markersize = 2)

ax1.legend(loc = 'best')
ax1.set_ylabel('Temperature \n $^\circ C$') 
# ax1.tick_params(labelsize = 11)
ax1.grid()
ax1.axis([0, 2.9, 26, 100])

ax1.set_xlabel('Time \n h')
plt.tight_layout()
if save_figs:
    print('saved')
    fig2.savefig(datadir / r'Figures/FOD2MOD.png', dpi = 300)
plt.show()