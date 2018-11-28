import rm;
import flatworkload;
import reservedpool;
import staticrm;
import env;

# System capacity
SC = 1000

# initial resource manager
rm = StaticRM(SC)

# initial environment
env = Env(rm)

# system contain 1 reserved pool with weight = 1
env.add_pool(POOL_RESERVED, ReservedPool(1))

env.add_workload("flat", FlatWorkload(100, 10))

# Run experiment for 1000 time unit
env.run(1000)

print(env.workloads["flat"].value())


