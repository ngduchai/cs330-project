
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
from mixedvaworkload import MixedVAWorkload

def plot_values(p, va, pname):
    plt.plot(p, va, labels = 'Video Analytic')
    plt.legend(loc='upper right')
    plt.ylabel('Value (V)')
    plt.xlabel('Rva')
    plt.title(pname)

# System capacity
SC = 81000
# SC = 453600 * 2
# Experiment length
#exp_time = 1 * 30 * 60 * 60 # An hour
exp_time = 30 * 60 * 30 # 30 mins
# Pool names
BURST_POOL = "burst"
ONDEMAND_POOL =  "on-demand"

# The parameters for the VA workload is chosen to be as close to the realistic as possible
lamb = 1 / float(10 * 60 * 30) # happen 1 per 10 mins
value_per_slot = 10
normal_load = 1
burst_height = normal_load * 140
task_size = 5
burst_width = 1 * 60 * 30 # burst last for 1 min
timeliness = 1.00001

ondemand_min_len = 1 * 60 * 30 # on-demand pool charge for at least 1 min

# Varied parameters
# minmum percentage of resource reserved for mRva such that there is at least one burst happen
#mRva = int(float(burst_height) / (1/lamb / burst_width))
#mRva = (int(mRva / 10) + 1) * 10
#mRva = 0
#Rva = np.array(list(range(mRva, SC+1)))
Rbp = np.array(list(range(0, 11)))
Rod = [10]*11-Rbp
task_guarantee = 30
# Rbp = [10]
# Rod = [0]

# Experiment outcomes
Values = [] # Total values
OpValues = [] # Optimal value
OpPartition = [] # Optimal partition

guarantee = np.array(list(range(1, 31)))
# initialize VA workload
# va_workload = VAWorkload(lamb, value_per_slot, normal_load,
        # burst_height, burst_width, timeliness, task_size, ONDEMAND_POOL)
va_workload = MixedVAWorkload(0, lamb, value_per_slot, normal_load,
        burst_height, burst_width, timeliness, task_size, ONDEMAND_POOL, BURST_POOL)
va_workload.setup(exp_time)

# Parameter to be varied
# dn  = np.array(list(range(1000, 160001, 5000)))
dn  = np.array([1])
# Run experiments by varying a parameter
pname = 'value per slot (w) = '
stddevs = np.array(range(2, 7, 1)) * 60 * 30
print stddevs
for stddev in stddevs:
    value = []
    for i in range(len(Rbp)):
        gc.collect()
        start = time.time()
        
    # initialize resource manager
    rm = StaticRM(SC)
    # initialize environment
    env = Env(rm)
    
    # initialize workloads 
    va_workload.restart()
    va_workload.stddev_runtime = stddev
    #va_workload.ratio = float(Rbp[i]) / 10.0
    
    env.add_workload("va", va_workload)
    # system contain 2 on-demand pools, one for flat and another for VA
    burst_pool = BurstPool(1, 15, 0)
    ondemand_pool = OnDemandPool(ondemand_min_len, 0)

    env.add_pool(BURST_POOL, burst_pool)
    env.add_pool(ONDEMAND_POOL, ondemand_pool)

    # Run experiment
    env.run(exp_time)

    # Get outcome
    va = env.workloads["va"].value()
    value.append(va)
    count = 0
    for task in va_workload.finished_tasks:
        if task.resource != va_workload.normal_load:
            count += 1
    print count
    
    end = time.time()
    # print "Progress:", i, "per", len(Rod)
    print " ---- Partition: burst pool =", burst_pool.capacity, "on-demand pool =", ondemand_pool.capacity
    print " ---- stddev", stddev, ",", va, "," ,burst_pool.acc_cost+ondemand_pool.acc_cost
    print " ---- Time:", end - start, "seconds"
        
        # initialize workloads 
        va_workload.restart()
        env.add_workload("va", va_workload)
        # system contain 2 on-demand pools, one for flat and another for VA
        burst_pool = BurstPool(Rbp[i], task_guarantee, 0)
        ondemand_pool = OnDemandPool(ondemand_min_len, Rod[i])

        env.add_pool(BURST_POOL, burst_pool)
        env.add_pool(ONDEMAND_POOL, ondemand_pool)

        # Run experiment
        env.run(exp_time)

        # Get outcome
        va = env.workloads["va"].value()
        value.append(va)
        count = 0
        for task in va_workload.finished_tasks:
            if task.resource != va_workload.normal_load:
                count += 1
        print count
        
        end = time.time()
        # print "Progress:", i, "per", len(Rod)
        print " ---- Partition: burst pool =", burst_pool.capacity, "on-demand pool =", ondemand_pool.capacity
        print " ---- Value: value =", va, "cost =",burst_pool.acc_cost+ondemand_pool.acc_cost
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



