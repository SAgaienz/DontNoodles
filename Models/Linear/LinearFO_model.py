import numpy as np 
import pandas 
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit, fsolve
from scipy.signal import lti, lsim
from scipy.interpolate import interp1d

df_Aux = pandas.read_csv('Data\Cleaned_70L_Step_data.csv')
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

tspan = np.linspace(0, 11000, 20000)

# Time that we turned the element on at (unit step)
def U(t):
    if t<t_on:
        return 0
    if t>=t_on:
        return 3000
        
# First order Model
def fo(tspan, K, τ ):
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

for V in [30, 40,50,60,70,80,90]:
    plt.plot(tspan, fo(tspan, *Params(V)), label = 'Volume = ' + str(V)+' L')
plt.plot(xdata, ydata, label = 'Volume = 70 L (Experimental Data)')
plt.legend(loc = 'best')
plt.ylabel('Temperature, °C')
plt.xlabel('Time, s')
plt.axis([-15, 11000,25, 100 ])
plt.savefig('Figures/Model Steps/Linear Model/Linear_Model_V.png', dpi = 200)
plt.show()