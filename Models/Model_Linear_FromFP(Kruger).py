# %%
import numpy as np
import sympy
import scipy
import matplotlib.pyplot as plt
# from sklearn import datasets
from sympy import fraction
from scipy import signal as sig
sympy.init_printing()


# %%
Te, Tw, Tp, Ti, Q, Ts = sympy.symbols('T_e, T_w, T_p, T_i, Q, T_s')
hw, ha, kp, ki = sympy.symbols('h_w, h_a, k_p, k_i')
Ae, Ap, Ai, As = sympy.symbols('A_e, A_p, A_i, A_s')
me, mw, mp, mi, Cpe, Cpw, Cpp, Cpi = sympy. symbols('m_e, m_w, m_p, m_i, Cp_e, Cp_w, Cp_p, Cp_i')
tp, ti, s = sympy.symbols('t_p, t_i, s')


# %%
EQ1 = (1/((me*Cpe)*s   +  (hw*Ae)))*Q + ((hw*Ae)/((me*Cpe)*s   +  (hw*Ae)))*Tw
EQ2 = ((hw*Ae)/((mw*Cpw)*s   + (hw*Ae)  +   (kp*Ap/tp) ))*Te   +   ((ha*Cpi)/((mw*Cpw)*s   + (hw*Ae)  +   (kp*Ap/tp) ))*Tp
EQ3 = ((kp*Ap/tp)/((mp*Cpp)*s   + (kp*Ap/tp)  +    (ki*Ai/ti) ))*Tw    +     ((ki*Ai/ti)/((mp*Cpp)*s   + (kp*Ap/tp)  +    (ki*Ai/ti) ))*Ti
EQ4 = ((ki*Ai/ti)/((mi*Cpi)*s  +    (ki*Ai/ti)    +     (ha*As)  ))*Tp  +     ((ha*As)/((mi*Cpi)*s  +    (ki*Ai/ti)    +     (ha*As)  ))*Ts

# %% [markdown]
# EQ4 in EQ3 (by $T_i$) ---> and 'EQ5' = $T_p$

# %%
EQ5 = EQ3.subs(Ti, EQ4)
EQ5 - Tp


# %%
EQ5 = sympy.solvers.solve(EQ5 - Tp, Tp)[0].simplify()
EQ5

# %% [markdown]
# EQ5 in EQ2 (by $T_p$) ---> and 'EQ6' = $T_w$

# %%
EQ6 = EQ2.subs(Tp, EQ5)
EQ6


# %%
EQ6 = sympy.solvers.solve(EQ6 - Tw, Tw)[0].simplify()
EQ6

# %% [markdown]
# Now the mess above is $T_w = TF(T_e, T_s)$. Now we sub EQ1 ('EQ1' = $T_e$) in for $T_e$ in the above...

# %%
Final = sympy.solvers.solve(EQ6.subs(Te, EQ1) - Tw, Tw)[0]


# %%
n, d = fraction(Final)


# %%
print('Order of Transfer Function:',  sympy.degree(d, s))
print('Order of Dynamics of Transfer Function:',  sympy.degree(n, s))

# %% [markdown]
# List of Coefficients of denominator of Transfer Function

# %%
deno = sympy.Poly(d, s)


# %%
nume = sympy.Poly(n, s)


# %%
nume2 = sympy.Poly(n, Q)


# %%
from sympy.abc import V


# %%
def vth(V): #V in Liters (always), returns tun level height (in meters)
    V = V/1000 #m3
    return V/((np.pi*(0.53**2))/(4))

m_w = lambda V: 1.000835560037227*V
A_p = lambda V: 0.00754779739983042*V
A_i = lambda V: A_p(V)


# %%
SubTF = Final.subs({ha: 10, Cpe: 450, Ae: 0.020734, me: 0.3, hw: 3750,
            Cpw: 4189.1473, kp: 0.453,  mp: 5, Cpp: 2e3,  ki:  0.013, ti:  22.5e-3, mi: 2,  Cpi: 0.1, 
                    As: 0.9952565526572466,  tp: 0.0045, mw: m_w(V), Ap: A_p(V), Ai: A_i(V)})


# %%
Servo = sympy.simplify(SubTF.expand()).subs({Ts: 0, Q: 1})


# %%
Servo


# %%
TF = sympy.lambdify(V, Servo)


# %%
TF(50)

# %% [markdown]
# Simulation:

# %%
def Q_in(t):
    if t>=0 and t< 500:
        return 0
    elif t>=500 :
        return 3000
#     elif t>=12600:
#         return 0


# %%
def SIM(tf, V = 40):    
    tspan = np.linspace(0, tf*3600, 1001)
    tspan2 = np.linspace(0, tf, 1001)
    a, b = fraction(TF(V))
    a1 = sympy.Poly(a)
    b1 = sympy.Poly(b)
    TwQ = sig.lti([float(a1.coeffs()[i]) for i in range(0, len(a1.coeffs()))], [float(b1.coeffs()[i]) for i in range(0, len(b1.coeffs()))])
    _, resp, _ = sig.lsim(TwQ, [Q_in(t) for t in tspan], tspan)
    resp = [resp[i] + 22 for i in range(0, len(resp))]
    return tspan2, resp


# %%
Vspan = [30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]


# %%
plt.plot(*SIM(10, 100))


# %%
plt.plot(*SIM(6, 80))
plt.show()


# %%
print(TF(V))


# %%
for i in [20, 30, 40, 50, 100]:
    plt.plot(*SIM(6, i))
plt.show()

# %%


# %%

# %%
