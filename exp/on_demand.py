
# IMPORTANT: Run the experiment inside its directory

import sys
sys.path.insert(0, './..')

import matplotlib.pyplot as plt
import numpy as np

import rm as common;
from flatworkload import FlatWorkload;
from vaworkload import VAWorkload;
from ondemandpool import OnDemandPool;
from staticrm import StaticRM;
from env import Env;
from reservedpool import ReservedPool

def plot_values(p, va, rf, pname):
    plt.stackplot(p, va, rf, labels = ['Video Analytic', 'Flat'])
    plt.legend(loc='upper right')
    plt.ylabel('Value (V)')
    plt.xlabel('Rva')
    plt.title(pname)

# System capacity
SC = 350
# Experiment length
time = 1 * 30 * 60 * 60 # An hour
#time = 10 * 30 * 60 # 15 mins
# Pool names
POOLNAME_BURST = "on-demand-burst"
POOLNAME_FLAT =  "on-demand-flat"

# The parameters for the VA workload is chosen to be as close to the realistic as possible
lamb = 1 / float(10 * 60 * 30) # happen 1 per 10 mins
value_per_slot = 10
normal_load = 1
burst_height = normal_load * 140
task_size = 10
burst_width = 1 * 60 # burst last for 1 min
timeliness = 1.01

# The parameters for the flat workload
flat_value = 1
flat_load = 280
flat_task_size = 10

ondemand_min_len = 1 * 60 * 30 # on-demand pool charge for at least 1 min

# Varied parameters
mRva = 0 # minmum percentage of resource reserved for mRva
#Rva = np.array(list(range(mRva, SC+1)))
Rva = np.array(list(range(mRva, SC+1, 50)))
Rsf = SC - Rva

# Experiment outcomes
Vva = [] # Value for VA workload
Vrf = [] # Value for foreground workload
Values = [] # Total values
OpValues = [] # Optimal value
OpPartition = [] # Optimal partition

# initialize VA workload
va_workload = VAWorkload(lamb, value_per_slot, normal_load,
        burst_height, burst_width, timeliness, task_size, POOLNAME_BURST)
va_workload.setup(time)

# Parameter to be varied
#dn  = np.array(list(range(1000, 160001, 5000)))
dn  = np.array([1, 2])
# Run experiments by varying a parameter
pname = 'value per slot (w) = '
for w in dn:
    value = []
    vas = []
    rfs = []
    for i in range(len(Rva)):
        # initialize resource manager
        rm = StaticRM(SC)
        # initialize environment
        env = Env(rm)
        
        # initialize workloads 
        flat_workload = FlatWorkload(flat_load, flat_task_size, flat_value, POOLNAME_FLAT)
        env.add_workload("flat", flat_workload)
        va_workload.restart()
        print va_workload.wait_for_burst, va_workload.burst_time
        env.add_workload("va", va_workload)
    
        # system contain 2 on-demand pools, one for flat and another for VA
        #burst_pool = OnDemandPool(ondemand_min_len, Rva[i])
        burst_pool = ReservedPool(Rva[i])
        env.add_pool(POOLNAME_BURST, burst_pool)
        #flat_pool = OnDemandPool(ondemand_min_len, Rsf[i])
        flat_pool = ReservedPool(Rsf[i])
        env.add_pool(POOLNAME_FLAT, flat_pool)

        # Run experiment
        env.run(time)
        
        # Get outcome
        va = env.workloads["va"].value()
        vas.append(va)
        rf = env.workloads["flat"].value()
        rfs.append(rf)
        value.append(va + rf)
        print "Progress:", i, "per", len(Rva)
        print " ---- Partition: va =", burst_pool.capacity, "flat =", flat_pool.capacity
        print " ---- Value: va =", va, "flat =", rf
        
    Vva.append(vas)
    Vrf .append(rfs)
    Values.append(value)
    OpValues.append(max(value))
    OpPartition.append(np.argmax(np.array(value)))

# Plot graphs
plt.figure(1)
dt = 0
plot_values(Rva, Vva[dt], Vrf[dt], pname + str(dn[dt]))

plt.figure(2)
#dt = int(len(dn) / 2) - 1
dt = 1
plot_values(Rva, Vva[dt], Vrf[dt], pname + str(dn[dt]))

#plt.figure(3)
#dt = len(dn) - 1
#plot_values(Rva, Vva[dt], Vrf[dt], pname + str(dn[dt]))

plt.figure(4)
plt.plot(dn, np.array(OpPartition))
plt.ylabel('Optimal Rva')
plt.xlabel('w');
plt.show()



