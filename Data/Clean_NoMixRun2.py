from datetime import datetime
import numpy as np 
import pandas 
# Parsing and cleaning....
df_raw = pandas.read_csv('Data/NoMixRun2.csv')
is_Aux = df_raw['name'] == 'AUX'
df_Aux = df_raw[is_Aux]
df_Aux = df_Aux.reset_index(drop=True)
tshift = 500*(1.5)
s_start_index = 625
s_stop_index = 643
df_Aux = df_Aux.drop(df_Aux.index[s_start_index: s_stop_index])

def time_delta_parser(t_str, t0_str):
    date_format = "%Y-%m-%dT%H:%M:%S.%f"
    t0 = datetime.strptime(t0_str, date_format)
    t = datetime.strptime(t_str, date_format)
    return (t-t0).total_seconds()

time_str_list = df_Aux['time'].tolist()

time_new = [time_delta_parser(i, df_Aux['time'][0]) for i in df_Aux['time'].tolist()]
df_Aux['time'] = time_new
ls = []
for i in df_Aux.index:
    t = df_Aux['time'][i]
    if i < s_stop_index:
        ls.append(t)
    if i >= s_stop_index:
        ls.append(t + tshift)
df_Aux['time'] = ls

df_Aux.to_csv('Data/Cleaned_70L_Step_data.csv')