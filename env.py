
import random;

class Env:
    def __init__(self, rm):
        self.rm = rm
        self.workloads = {}
        self.pools = {}

    def add_workload(name, workload):
        self.workloads[name] = workload

    def add_pool(name, pool);
        self.pools[name] = pool
        self.rm.add_pool(pool)

    def run(length):
        # first, let resource manager assign resources to pools
        rm.adjust_partition()
        # run experiment for [length] time slot
        for time in range(length):
            # check for new tasks from workload
            new_tasks = []
            for workload in self.workloads:
                new_tasks.append(workload.make_request())
            
            # shuffle task to ensure fairness
            random.shuffle(new_tasks)
            
            # redirect request to pools
            waiting_list = {}
            for task in new_tasks:
                # update arrival time for each task
                task.arrival_time = time
                if task.pool not in waiting_list
                    waiting_list[task.pool] = []
                waiting_list[task_pool].append(task)
            
            # lunch tasks in pools and get finished tasks in the current time slot
            finished_tasks = []
            for key, task_list in waiting_list.iteritems():
                finish_list.append( pools[key].launch_task(task_list) )

            # notify workloads about finished tasks
            for task in finished_task:
                # update finish time for task
                task.finish_time = time + 1 
                task.workload.update([task])
            
            # finnally, let the resource manager adjust its partition
            rm.adjust_partition();

                

