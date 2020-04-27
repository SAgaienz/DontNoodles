import numpy as np 
import pandas 
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit
from scipy.signal import lti, lsim

df = pandas.read_csv('Data/70L_Step_data_Cleaned.csv')

xdata, ydata = df['time'].tolist(), df['tem'].tolist()
xdata1, ydata1 = xdata[0:1400], ydata[0:1400]


st = 33.358
T0 = np.mean(ydata[0:5])
tspan = np.linspace(0, 9000, 2000)

t_to_boil = 4.186*70*(ydata[-1] - ydata[0])/3
print(t_to_boil)

def U(t):
    if t<st:
        return 0
    if t>=st:
        return 3000

def fo(tspan, K, τ ):
    Uspan = [U(t) for t in tspan]
    Gp = lti(K, [τ , 1 ])
    _, Tl, _ = lsim(Gp, Uspan, tspan)
    Tl = Tl + T0
    return Tl

B, res =  curve_fit(fo, xdata1, ydata1, [100000, 5000])
plt.plot(tspan, fo(tspan, *B), label = 'FO model' , color = '#c2510c')
plt.plot(xdata, ydata, label = 'Exp Data from 70L Step Test', color = '#10bbc7')
plt.text(1500,30, 'K = '+ str(B[0]) + ',  τ = '+ str(B[1])  )
plt.legend(loc = 'best')
plt.show()
