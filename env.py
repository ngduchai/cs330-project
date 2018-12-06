
import random;
import time as tm

class Env:
    def __init__(self, rm):
        self.rm = rm
        self.workloads = {}
        self.pools = {}

    def add_workload(self, name, workload):
        self.workloads[name] = workload

    def add_pool(self, name, pool):
        self.pools[name] = pool
        self.rm.add_pool(pool)

    def run(self, length):
        # first, let resource manager assign resources to pools
        self.rm.adjust_partition()
        # run experiment for [length] time slot
        for time in range(length):
            # check for new tasks from workload
            pools = {}
            for _, workload in self.workloads.iteritems():
                workload.make_request(time, pools)
            
            # shuffle task to ensure fairness
            #random.shuffle(new_tasks)
            
            # redirect request to pools
            #waiting_list = {}
            #for task in new_tasks:
                # update arrival time for each task
            #    task.arrival_time = time
            #    if task.pool not in waiting_list:
            #        waiting_list[task.pool] = []
            #    waiting_list[task.pool].append(task)
            
            # lunch tasks in pools and get finished tasks in the current time slot
            #finished_tasks = []
            #for key, task_list in waiting_list.iteritems():
            #    finished_tasks += self.pools[key].launch_task(task_list)
            #    for task in self.pools[key].launch_task(task_list):
            #        task.finish_time = time + 1
            for key, task_list in pools.iteritems():
                self.pools[key].launch_task(time, task_list)

            # For performance improvement, workload has been already updated by the pool
            # notify workloads about finished tasks
            #updated_tasks = {}
            #for task in finished_tasks:
            #    # update finish time for task
            #    task.finish_time = time + 1
            #    if task.workload not in updated_tasks:
            #        updated_tasks[task.workload] = []
            #    updated_tasks[task.workload].append(task)
            #for workload, task_list in updated_tasks.iteritems():
            #    workload.update(task_list)
            
            # finnally, let the resource manager adjust its partition
            self.rm.adjust_partition();

                

