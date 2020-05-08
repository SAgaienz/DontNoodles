import numpy as np 
import matplotlib.pyplot as plt 
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d
import pandas
## Still working on it
def R_evap2(T, V, U, args):
    Ts, Tboil, h, T_evap_start = args
    σ = 5.67e-8
    r_evap_max = (3000 - A_p_V(V)*h*(Tboil - Ts) - A_p_V(V)*σ*(Tboil**4 - Ts**4))/ 2396.4e3
    mdpnt = (Tboil + T_evap_start)/2
    b = 0.9
    κ = lambda U: (1/3000) *U
    return r_evap_max/(1 + np.exp(-b*(T - mdpnt)))*κ(U)