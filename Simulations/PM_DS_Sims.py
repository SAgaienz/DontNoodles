#%%
import numpy as np 
import tbcontrol.blocksim as bl 
import matplotlib.pyplot as plt 

T0 = 22
U = lambda t: 0*np.heaviside(t, 1) + (40-0)*np.heaviside(t-3600, 1) + (80 - 40)*np.heaviside(t-11000, 1) + (0-80)*np.heaviside(t-(5.4*3600), 1) + T0

#%%
def params(V):
    Kp = (95-22)/3000
    [A1, B1], [A2, B2 ]= [[  5.24404762, 182.26190473],  [0.01010714, 0.73178571]]
    τ, ζ = [A1*V + B1  , A2*V + B2]
    return [Kp, τ , ζ]

#%%
def time_to_boil(Tf, V):
    Cp = 4.186
    t = (Cp*V*(Tf - 22)*1000*1.1)/3000
    return t


def Controller(V, α):
    Kp, τp, ζp = params(V)
    τc = τp*α    
    Kc = (2*τp*ζp)/(Kp*τc)
    τI = Kp*τc
    τD = (τp**2)/(Kp*τc)
    return [Kc, τI, τD]

#%%

ts = np.linspace(0, 25000, 250001)
#%%
def Resp(V, α):
    Kc, τI, τD = Controller(V, α)
    Kp, τp, ζp = params(V)
    Km, τm = 1, 17.906

    Gp = bl.LTI('Gp', 'Q', 'T', [Kp], [τp, 2*τp*ζp, 1])
    Gc = bl.PID('Gc', 'E', 'Q', Kc, τI, τD)
    Gm = bl.LTI('Gm', 'T', 'Tm', [Km], [τm, 1])

    blocks = [Gp, Gc, Gm]
    sums = {'E': ('+Tsp', '-Tm')}
    inputs = {'Tsp': lambda t: U(t) - T0}

    diagram = bl.Diagram(blocks, sums, inputs)
    res = np.array(diagram.simulate(ts)['T'])
    return [r + T0 for r in res]
#%%
Vspan = [30,40,50,60,70,80,90,100]
# Vspan = [30]

Tlist = [time_to_boil(62, V)+3600 for V in Vspan]

for V in Vspan:
    plt.plot(ts, Resp(V, 12.6), label = 'V = ' + str(V) + 'L')
plt.plot(ts, [U(t) for t in ts])
plt.legend(loc = 'upper left')
plt.xlabel('time')
plt.grid(True)
plt.ylabel('temperature')
plt.show()
#%%
# plt.plot(ts, [U(t) for t in ts])
# plt.show()

# %%
