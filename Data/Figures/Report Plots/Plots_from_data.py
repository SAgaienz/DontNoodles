# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np 
from matplotlib import cm, rc
import scipy.signal as sig 
from scipy.optimize import curve_fit
from datetime import datetime


# %%
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)


# %%
HLT = pd.read_csv('/home/zephyr/Internal/UserData/Documents/ChemEng/CSC/CSC411 Source Code Repo/Data/NMHLT.csv')
BK = pd.read_csv('/home/zephyr/Internal/UserData/Documents/ChemEng/CSC/CSC411 Source Code Repo/Data/NMBK.csv')
MT = pd.read_csv('/home/zephyr/Internal/UserData/Documents/ChemEng/CSC/CSC411 Source Code Repo/Data/NMMT.csv')
AUX = pd.read_csv('/home/zephyr/Internal/UserData/Documents/ChemEng/CSC/CSC411 Source Code Repo/Data/NMAUX.csv')
def fun(df):
    return [[i/60 for i in df['t'].tolist() ], df['T'].tolist()]
save_figs = True


# %%
fig1 = plt.figure(figsize=[6,6])
cols = [cm.viridis(x) for x in np.linspace(0, 1, 4)]
plt.plot(*fun(BK), label = 'S1 - Beneath Element', color = cols[0])
plt.plot(*fun(HLT), label = 'S2 - Shallow, Wall Above Element', color = cols[1])
plt.plot(*fun(MT), label = 'S3 - Shallow, Opposite Wall Above Element' , color = cols[2])
plt.plot(*fun(AUX), label = 'S4 - Directly Above Element', color = cols[3])

plt.legend(loc = 'best')
plt.xlabel('Time \n min', fontsize = 11)
plt.ylabel('Temperature \n $^ \circ C$', fontsize = 11) 
plt.tight_layout()
plt.tick_params(labelsize = 11)
plt.grid()
if save_figs:
    print('saved')
    fig1.savefig('/home/zephyr/Internal/UserData/Documents/ChemEng/CSC/CSC411 Report Repo/Figures/Data/Fd1_70L.png', dpi = 300)
plt.show()


# %%



# %%
HLT = pd.read_csv('/home/zephyr/Internal/UserData/Documents/ChemEng/CSC/CSC411 Source Code Repo/Data/Cleaned_70L/HLT.csv')
BK = pd.read_csv('/home/zephyr/Internal/UserData/Documents/ChemEng/CSC/CSC411 Source Code Repo/Data/Cleaned_70L/BK.csv')
MT = pd.read_csv('/home/zephyr/Internal/UserData/Documents/ChemEng/CSC/CSC411 Source Code Repo/Data/Cleaned_70L/MT.csv')
AUX = pd.read_csv('/home/zephyr/Internal/UserData/Documents/ChemEng/CSC/CSC411 Source Code Repo/Data/Cleaned_70L/AUX.csv')
def fun(df):
    return [[i/60 for i in df['time'].tolist() ], df['tem'].tolist()]
# print(MT)


# %%
fig2 = plt.figure(figsize=[6,6])
cols = [cm.viridis(x) for x in np.linspace(0, 1, 4)]
plt.plot(*fun(BK), label = 'S1 - Beneath Element', color = cols[0])
plt.plot(*fun(HLT), label = 'S2 - Shallow, Wall Above Element', color = cols[1])
plt.plot(*fun(MT), label = 'S3 - Shallow, Opposite Wall Above Element' , color = cols[2])
plt.plot(*fun(AUX), label = 'S4 - Directly Above Element', color = cols[3])

plt.legend(loc = 'best')
plt.xlabel('Time \n min', fontsize = 11)
plt.ylabel('Temperature \n $^ \circ C$', fontsize = 11) 
plt.tight_layout()
plt.tick_params(labelsize = 11)
plt.grid()
if save_figs:
    print('saved')    
    fig2.savefig('/home/zephyr/Internal/UserData/Documents/ChemEng/CSC/CSC411 Report Repo/Figures/Data/Fd2_Clean_70L.png', dpi = 300)
plt.show()


# %%
df_raw = pd.read_csv('/home/zephyr/Internal/UserData/Documents/ChemEng/CSC/CSC411 Source Code Repo/Data/ProbeDynamics.csv')
is_Aux = df_raw['name'] == 'AUX'
df_Aux = df_raw[is_Aux]
df_Aux = df_Aux.reset_index(drop=True)
df_Aux = df_Aux[0:113]
def time_delta_parser(t_str_ls):
    date_format = "%Y-%m-%dT%H:%M:%S.%f"
    ls = []
    t0 = datetime.strptime(t_str_ls[0], date_format)
    for t in t_str_ls:
        dt_item = datetime.strptime(t, date_format)
        ls.append((dt_item - t0).total_seconds())

    return ls

time_str_list = df_Aux['time'].tolist()

#data we can use to fit FO model:
d_time = time_delta_parser(time_str_list)
d_temp = [i - df_Aux['tem'].tolist()[0] for i in df_Aux['tem'].tolist()]

xdata, ydata = d_time, d_temp

def U(t):
    if t<196:
        return 0
    if t>=196:
        return 72

def resp(xdata, K, τ):
    res = []
    for x in xdata:
        if x<196:
            r = 0
        if x>=196:
            r = ((K*(np.exp((x-196)/τ) - 1)*np.exp(-(x-196)/τ))*72)
        res.append(r)
    return res


# %%
print(beta)


# %%
save_figs = True
cols = [cm.viridis(x) for x in np.linspace(0, 1, 3)]
tspan = np.linspace(0, 500, 1000)
beta, resid = curve_fit(resp, xdata, ydata, p0 = [1, 16])
fig3 = plt.figure(1, figsize = (5.5,5.5))
plt.plot(xdata, [y + 22 for y in ydata], label = 'Experimental DS18b20 Sensor Repsonse', ls = '', marker = 'o', color = cols[1])
plt.plot(tspan, [i + 22 for i in resp(tspan, *beta)],  color = cols[2], label = r'First-Order Model')
plt.plot(tspan, [U(x)+22 for x in tspan], label = 'Probe Unit Step (T(s) = 72/s)', color = cols[0])
plt.legend(loc = 'upper left')
# plt.legend(loc = 'best')
plt.xlabel('Time \n s', fontsize = 12)
plt.ylabel('Temperature \n $^ \circ C$', fontsize = 11) 
plt.text(305, 34, r'K = ' + str(np.round(beta[0], 2)))
plt.text(305, 30, r'$\tau$ = ' + str(np.round(beta[1], 3)) + ' s')
plt.tight_layout()
plt.axis([-13,426,10,115])
plt.tick_params(labelsize = 11)
plt.grid()
if save_figs:
    print('saved')
    plt.savefig('/home/zephyr/Internal/UserData/Documents/ChemEng/CSC/CSC411 Report Repo/Figures/ProbeDynamicsPlot.png', dpi = 300)
plt.show()


# %%



# %%



# %%


