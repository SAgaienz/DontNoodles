# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import numpy as np 
from scipy.optimize import curve_fit
from scipy.signal import lsim, lti
import matplotlib.pyplot as plt
from ipywidgets import interact
import pandas as pd
from matplotlib import cm, rc
cols = [cm.viridis(i) for i in np.linspace(0, 1, 2)]


# %%
df = pd.read_csv('/home/zephyr/Documents/ChemEng/CSC/CSC411 Source Code Repo/Data/Cleaned_70L/AUX.csv')
xdata, ydata = df['time'], df['tem']
save_figs = False


# %%
def U(t):
    if t<33:
        return 0
    else:
        return 3000
T0 = np.mean(df['tem'].tolist()[0:5])
tspan = np.linspace(0, df['time'].tolist()[-1], len(df['time'].tolist()))
def SO(tspan, z, τ ):
    Uspan = [U(t) for t in tspan]
    K = 23e-3
    Gp = lti(K, [τ**2, 2*τ*z , 1 ])
    _, Tl, _ = lsim(Gp, Uspan, tspan)
    Tl = Tl + T0
    return Tl


# %%
B, R = curve_fit(SO, xdata, ydata, p0 =[1.5, 2000] )
B


# %%
# t1 = ('K = 0.023 $^\circ C / W$')
# t2 = ('τ = 36.784 min')
# t3 = ('ζ = 0.8895')


# %%
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

tspan2 = np.linspace(0,3*3600, 1000)
fig1, ax1 = plt.subplots(1,1, sharex = True ,figsize=[6.5,6])
cols = [cm.viridis(i) for i in np.linspace(0, 1, 3)]
ax1.plot([t/3600 for t in tspan2], SO(tspan2, *B), color = cols[0], label = 'Second-Order Transfer Function Model')
ax1.plot([x/3600 for x in xdata], ydata, color = cols[1], label = '70 L Experimental Data')
ax1.legend(loc = 'best')

ax1.set_ylabel('Temperature \n $^\circ C$', fontsize = 11) 
ax1.tick_params(labelsize = 11)
ax1.grid()
ax1.axis([0, 2.7, 26, 100])
ax1.text(2, 45, r'K = 0.023 $^\circ C / W$')
ax1.text(2, 40, r'$\tau$ = 36.784 min')
ax1.text(2, 32, r'$ \zeta$ = 0.8895')
# ax2 = ax1.twinx()

# ax2.plot(tspan2, [U(t) for t in tspan2], color = 'r')
# ax2.axis([0, 2.7, 26, 5000])
# ax2.set_ylabel('Element Power Input \n $W$', fontsize = 11)
ax1.set_xlabel('Time \n h', fontsize = 11)
# plt.tight_layout()
if save_figs:
    print('saved')
    fig1.savefig('/home/zephyr/Documents/ChemEng/CSC/CSC411 Report Repo/Figures/SOMOD.png', dpi = 300)
plt.show()


# %%



