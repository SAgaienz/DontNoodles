import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 

df = pd.read_csv('70L_comp.csv')
plt.plot(df['time'], df['tem'])
plt.show()