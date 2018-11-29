
# IMPORTANT: Run the test inside its directory

import sys
sys.path.insert(0, './..')

import rm as common;
from flatworkload import FlatWorkload;
from reservedpool import ReservedPool;
from staticrm import StaticRM;
from env import Env;

# System capacity
SC = 1000

# initial resource manager
rm = StaticRM(SC)

# initial environment
env = Env(rm)

# system contain 1 reserved pool with weight = 1
env.add_pool(common.POOL_RESERVED, ReservedPool(1))

env.add_workload("flat", FlatWorkload(100, 10))

# Run experiment for 1000 time unit
env.run(1000)

print "Value of flat workload:", env.workloads["flat"].value()


