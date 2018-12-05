
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
pool.alloc(pool.requirement * 2)

time = 10000

workload = FlatWorkload(pool.requirement * 2, 5, 1, "burst") 

pool_tasks = {}
pool_tasks["burst"] = []
gok = True
last_finish = len(workload.finished_tasks)

for t in range(time):
    workload.make_request(t, pool_tasks)
    pool.launch_task(t, pool_tasks["burst"])
    if (t % 30 == 0):
        current_finish = len(workload.finished_tasks)
        print "Rate:", current_finished - last_finished 
        if current_finished - last_finished < 2:
            gok = False
            break
if gok:
    print "The pool works"
else:
    print "Something not good happened"

	
