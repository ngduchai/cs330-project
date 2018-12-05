
# IMPORTANT: Run the test inside its directory

import sys
sys.path.insert(0, './..')

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import math


import rm as common;
from reservedpool import ReservedPool;
from burstpool import BurstPool;
from staticrm import StaticRM;
from env import Env;
from vaworkload import VAWorkload
from flatworkload import FlatWorkload

pool = BurstPool(0, 0)
pool.alloc(pool.requirement)

print pool.requirement

time = 1000

workload = FlatWorkload(pool.requirement * 4, 5, 1, "burst") 

pool_tasks = {}
gok = True
last_finish = len(workload.finished_tasks)

for t in range(time):
    pool_tasks["burst"] = []
    workload.make_request(t, pool_tasks)
    pool.launch_task(t, pool_tasks["burst"])
    if (t % 30 == 0):
        current_finish = len(workload.finished_tasks)
        print "Rate at", t, ":", current_finish - last_finish 
        if current_finish - last_finish < 2:
            gok = False
            break
        last_finish = current_finish
if gok:
    print "The pool works"
else:
    print "Something not good happened"

	
