
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

pool = BurstPool(0, 3, 0)
pool.alloc(15)
print(pool.requirement)

time = 10

start_times = []
tasks = []

for t in range(time):
	new = common.Task(t, 0, 5, 3, pool, None)
	new2 = common.Task(t, 0, 5, 3, pool, None)
	pool.launch_task([new,new2])
	tasks.append(new)
	tasks.append(new2)
	for task in tasks:
		print(task.status),
	print()