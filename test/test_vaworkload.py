
# IMPORTANT: Run the test inside its directory

import sys
sys.path.insert(0, './..')

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import math


import rm as common;
from flatworkload import FlatWorkload;
from reservedpool import ReservedPool;
from staticrm import StaticRM;
from env import Env;
from vaworkload import VAWorkload

lamb = 0.1
value_per_slot = 10
normal_load = 0
burst_height = 100
burst_width = 1
timeliness = 1.01

va = VAWorkload(lamb, value_per_slot, normal_load, burst_height, burst_width, timeliness)

time = 1000000

start_times = []

for t in range(time):
    tasks = va.make_request()
    if len(tasks) != 0:
        task = tasks.pop()
        if task.resource == burst_height:
            start_times.append(t)

gaps = []
for i in range(len(start_times) - 1):
    gaps.append(start_times[i+1] - start_times[i])

print "Lambda =", lamb
print "Mean of interval between burst = ", np.mean(gaps)

x = np.linspace(0, max(gaps))
#y_pdf = lamb * np.exp(-lamb * x) + 1000
y_pdf = stats.expon.pdf(x, scale = 1 / lamb)

plt.hist(gaps, bins=100, density=True, histtype='stepfilled', alpha=0.2)
plt.plot(x, y_pdf, alpha=0.6)
plt.show()



