import pandas as pd 
import numpy as np 
import scipy.signal as sig 
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit
from datetime import datetime

from dataconfig import datadir

# from Models.ProbeDynamics.dataconfig import bulk_dir
# Parsing and cleaning....
df_raw = pd.read_csv(datadir / r'ProbeDynamics.csv')
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
            r = (K*(np.exp((x-196)/τ) - 1)*np.exp(-(x-196)/τ))*72
        res.append(r)
    return res

save_fig = str(input("save fig? (y/n)   "))

tspan = np.linspace(0, 500, 1000)
beta, resid = curve_fit(resp, xdata, ydata, p0 = [1, 16])
fig1 = plt.figure(1, figsize = (8,8))
plt.scatter(xdata, ydata, label = 'Probe Response (Tm(s)/T(s))')
plt.plot(tspan, resp(tspan, *beta), label = 'FO Model params: K = '+ str(np.round(beta[0], 3)) + ' , τ = '+ str(np.round(beta[1], 3)), color = 'r')
plt.plot(tspan, [U(x) for x in tspan], color = 'm', label = 'Probe Unit Step (T(s) = 72/s)')
plt.legend(loc = 'upper left')
plt.xlabel('Time \n seconds')
plt.ylabel('Temperature \n $^\circ C$')
plt.grid(True)
plt.axis([-13,426,-2.6,90])
if save_fig=='y':
    plt.savefig('Figures\ProbeDynamicsPlot.png', dpi = 200)
    plt.show()
else:
    plt.show()

