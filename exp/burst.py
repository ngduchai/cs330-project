
# IMPORTANT: Run the experiment inside its directory

import sys
sys.path.insert(0, './..')

import matplotlib.pyplot as plt
import numpy as np
import time
import gc

import rm as common;
from flatworkload import FlatWorkload;
from vaworkload import VAWorkload;
from ondemandpool import OnDemandPool;
from burstpool import BurstPool;
from staticrm import StaticRM;
from env import Env;
from reservedpool import ReservedPool

def plot_values(p, va, pname):
    plt.plot(p, va, labels = 'Video Analytic')
    plt.legend(loc='upper right')
    plt.ylabel('Value (V)')
    plt.xlabel('Rva')
    plt.title(pname)

# System capacity
SC = 350
# Experiment length
#exp_time = 1 * 30 * 60 * 60 # An hour
exp_time = 15 * 60 * 30 # 30 mins
# Pool names
BURST_POOL = "burst"
ONDEMAND_POOL =  "on-demand"

# The parameters for the VA workload is chosen to be as close to the realistic as possible
lamb = 1 / float(10 * 60 * 30) # happen 1 per 10 mins
value_per_slot = 10
normal_load = 1
burst_height = normal_load * 140
task_size = 10
burst_width = 1 * 60 * 30 # burst last for 1 min
timeliness = 1.01

ondemand_min_len = 1 * 60 * 30 # on-demand pool charge for at least 1 min

# Varied parameters
# minmum percentage of resource reserved for mRva such that there is at least one burst happen
#mRva = int(float(burst_height) / (1/lamb / burst_width))
#mRva = (int(mRva / 10) + 1) * 10
#mRva = 0
#Rva = np.array(list(range(mRva, SC+1)))
Rbp = np.array(list(range(0, int(1.1*350), int(0.1*350))))
Rod = SC - Rbp

# Experiment outcomes
Values = [] # Total values
OpValues = [] # Optimal value
OpPartition = [] # Optimal partition

# initialize VA workload
va_workload = VAWorkload(lamb, value_per_slot, normal_load,
        burst_height, burst_width, timeliness, task_size, BURST_POOL)
va_workload.setup(exp_time)

# Parameter to be varied
#dn  = np.array(list(range(1000, 160001, 5000)))
dn  = np.array([1])
# Run experiments by varying a parameter
pname = 'value per slot (w) = '
for w in dn:
    value = []
    for i in range(1):
        gc.collect()
        start = time.time()
        
        # initialize resource manager
        rm = StaticRM(SC)
        # initialize environment
        env = Env(rm)
        
        # initialize workloads 
        va_workload.restart()
        env.add_workload("va", va_workload)
        # system contain 2 on-demand pools, one for flat and another for VA
        burst_pool = BurstPool(ondemand_min_len, 5000)
        ondemand_pool = OnDemandPool(ondemand_min_len, 0)

        env.add_pool(BURST_POOL, burst_pool)
        # env.add_pool(ONDEMAND_POOL, ondemand_pool)

        # Run experiment
        env.run(exp_time)

        # Get outcome
        va = env.workloads["va"].value()
        value.append(va)
        print len(va_workload.finished_tasks)
        
        end = time.time()
        print "Progress:", i, "per", len(Rod)
        print " ---- Partition: burst pool =", burst_pool.capacity, "on-demand pool =", ondemand_pool.capacity
        print " ---- Value: value =", value
        print " ---- Time:", end - start, "seconds"
        
    Values.append(value)
    OpValues.append(max(value))
    OpPartition.append(np.argmax(np.array(value)))

# Plot graphs
# plt.figure(1)
# dt = 0
# plot_values(Rva, Vva[dt], pname + str(dn[dt]))

# #plt.figure(2)
# #dt = int(len(dn) / 2) - 1
# #dt = 1
# #plot_values(Rva, Vva[dt], Vrf[dt], pname + str(dn[dt]))

# #plt.figure(3)
# #dt = len(dn) - 1
# #plot_values(Rva, Vva[dt], Vrf[dt], pname + str(dn[dt]))

# plt.figure(4)
# plt.plot(dn, np.array(OpPartition))
# plt.ylabel('Optimal Rva')
# plt.xlabel('w');
# plt.show()



