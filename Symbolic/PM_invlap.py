#%%

from sympy import inverse_laplace_transform as ilt 
from sympy.abc import s, t, K
from sympy import symbols
from sympy import init_printing

#%%
τ, K, t, s, P = symbols('τ, K, t, s, P' , real =  True)

exp = (P/s)*(K/(τ*s + 1 ))
ilt(exp, s, t)