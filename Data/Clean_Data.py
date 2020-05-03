
import pandas as pd 
import scipy
import matplotlib.pyplot as plt
import numpy as np 
from dateutil.parser import parse 
from datetime import datetime
import scipy.signal as sig

df = pd.read_csv('I:/UserData/Documents/ChemEng/CSC/Lockdown/Data/NoMixRun2_failed.csv')


def Duration(df):
    tspan = [parse(t) for t in df['time'].tolist()]
    ts = []
    for t in tspan:
        dt = t - tspan[0]
        t_sec = dt.total_seconds()
        ts.append(t_sec)
    return ts


data = {}

for prb in ['HLT', 'BK', 'MT', 'AUX']:
    tems = df[df['name']==prb]['tem'].tolist()
    index = np.arange(0, len(df[df['name']==prb]))
    data[prb] = [Duration(df[df['name']==prb]) , tems, index]


data2 = {}
shift = (4596 - 4115) + (3884 - 3579)
for prb in data.keys():
    tspan, tems, index = data[prb]
    t_new = []
    for i in index:
        if i<627:
            t = tspan[i]
        elif i>627:
            t = tspan[i] + shift
        t_new.append(t)
    data2[prb] = [index, t_new, tems]

DF2 = pd.DataFrame(columns =['index' , 'time', 'tem'])

DF2['time'], DF2['tem'], DF2['index'] = data2['AUX'][1], data2['AUX'][2],  data2['AUX'][0]
for i in range(626, 626+14):
    DF2 = DF2.drop(i)
DF2 = DF2.drop(np.arange(1543, 1577))
DF2['index'] = np.arange(0, len(DF2['tem']))
DF2.index = DF2['index']
DF2.to_csv('Data/70L_Step_data_Cleaned.csv')

# f_T_index = scipy.interpolate.interp1d(DF2['tem'], DF2['index'])

### Plot
def U(t):
    if t<33.358:
        return 0
    if t>=33.358:
        return 3000
tspan1 = np.linspace(DF2['time'].tolist()[0], DF2['time'].tolist()[-1], 20000)

def plot_main():
    fig, ax1 = plt.subplots()
    plt.title('70 L Step Test')
    ax1.plot(DF2['time'], DF2['tem'])
    ax1.set_xlabel('Time, s')
    ax1.set_ylabel('Temperature, Celcius')

    ax2 = ax1.twinx()
    col2 = '#51a65c'
    ax2.plot(tspan1, [U(t) for t in tspan1], color = col2)
    ax2.set_ylabel('Element Power, kW', color = col2)
    ax2.tick_params(axis='y', labelcolor=col2)
    plt.savefig('Figures/70L_Cleaned_Data.png', dpi = 300)
    plt.show()
# plot_main()

plt.plot(tspan1, [((9.355e-3)*t + 26.5847) for t in tspan1])
plt.scatter(DF2['time'], DF2['tem'], alpha = 0.6, color = 'r')
plt.show()

# plt.subplot(1,2,1)
# plt.scatter(DF2['time'], DF2['tem'], alpha = 0.6, color = 'r')
# plt.subplot(1,2,2)
# plt.scatter(DF2['time'], DF2['index'], alpha = 0.6, color = 'b')
# plt.show()