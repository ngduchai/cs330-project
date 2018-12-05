
import common;

import matplotlib.pyplot as plt
import numpy as np

def plot_values(p, va, rf, pname):
    plt.stackplot(p, va, rf, labels = ['Video Analytic', 'Foreground'])
    plt.legend(loc='upper right')
    plt.ylabel('Value (V)')
    plt.xlabel('Rva')
    plt.title(pname)



# Set up unchanged parameters
lamb = 1e-5 # To avoid overlapping, the highest frequency should be 0.0005
h = 200
d = 900 # ~30 seconds of 30 fps deep processing
tau = 1.01 # value drop ~50 per min
c = 400
SC = 500
x = 1
w = 80000 #8

# Vary parameters
# Note that video analytic share must large enough to 
# ensure that there are at most 1 burst occur at anytime
mRva = int(h / (1/lamb / d))
Rvas = []
Rsfs = []

Vva = []
Vrf = []
Values = []
OpValue = []
OpPartition = []

# Parameters used for experiment
#dn = np.array(list(range(100010, 110001, 10))) / 100000.0;
dn = np.array(list(range(100010, 101001, 10))) / 100000.0;
pname = 'tau';
for tau in dn:
    value = []
    vas = []
    rfs = []
    
    mRva = int(h / (1/lamb / d))
    Rva = np.array(list(range(mRva, SC+1)))
    Rsf = SC - Rva

    for i in range(len(Rva)):
        va = common.compute_burst_value(lamb, h, d, w, tau, Rva[i])
        vas.append(va)
        rf = common.compute_foreground_value(c, x, Rsf[i])
        rfs.append(rf)
        value.append(va + rf)
    
    Vva.append(vas)
    Vrf.append(rfs)
    Rvas.append(Rva)
    Rsfs.append(Rsf)
    Values.append(value)
    OpValue.append(max(value))
    OpPartition.append(np.argmax(np.array(value)) + mRva)

#plt.stackplot(Rva, Vva[len(dn)-1], Vrf[len(dn)-1], labels = {'Video Analytic', 'Foreground'})
#plt.stackplot(Rva, Vva[len(dn)-1])
#plt.stackplot(Rva, Vrf[len(dn)-1])
#plt.legend(loc='upper left')
#plt.ylabel('Value (V)')
#plt.xlabel('Rva')
#plt.show();

plt.figure(1)
dt = 0
plot_values(Rvas[dt], Vva[dt], Vrf[dt], pname + ' = ' + str(dn[dt]))

plt.figure(2)
#dt = int(len(dn) / 2) - 1
dt = 19
plot_values(Rvas[dt], Vva[dt], Vrf[dt], pname + ' = ' + str(dn[dt]))

plt.figure(3)
dt = len(dn) - 1
plot_values(Rvas[dt], Vva[dt], Vrf[dt], pname + ' = ' + str(dn[dt]))

plt.figure(4)
plt.plot(dn, np.array(OpPartition))
plt.ylabel('Optimal Rva')
plt.xlabel(pname);
plt.show()








