import rm
import time as tm

class OnDemandPool(rm.Pool):
    def __init__(self, od_min_len, *args, **kwargs):
        super(OnDemandPool, self).__init__(*args, **kwargs)
        # self.free_capacity = 0
        self.shrink_capacity = 0
        self.od_min_len = od_min_len
        self.acc_cost = 0
        self.pending = {}

    def reclaim(self, unit):
        #reclaim resources
        #add unit to amount to be reclaimed shrink as much as possible
        self.shrink_capacity += unit
        if self.free_capacity >= self.shrink_capacity:
            # shrink by all of shrink_capacity
            self.free_capacity -= self.shrink_capacity
            self.shrink_capacity = 0
            return unit
        else:
            # shrink by free_capacity
            shrink_amt = self.free_capacity
            self.shrink_capacity -= shrink_amt
            self.free_capacity = 0
            return shrink_amt

    def launch_task(self, time, tasks):
        # add the task to running_task if enough resources, or reject
        #finished = []
        for i in range(len(tasks)):
            task = tasks[i]
            if task.resource <= self.free_capacity:
                self.free_capacity -= task.resource
                # self.running_tasks.append(task)
                task.status = rm.Status.RUNNING
                finish_time = time + task.runtime
                if finish_time not in self.pending:
                    self.pending[finish_time] = []
                self.pending[finish_time].append(task)
            else:
                # NOTE: we assume that the pool serves only 1 workload, which is true
                # in our scenarios
                if hasattr(task.workload, 'failed_ondemand_tasks'):
                    task.workload.failed_ondemand_tasks += tasks[i:]
                else:
                    task.workload.failed_tasks += tasks[i:]
                break
                #task.status = rm.Status.REJECTED
            
                # Break the interface for performance improvement
                #task.workload.failed_tasks.append(task)
                
                #finished.append(task)
        #print "accept task", end - start
        # run each task
        reclaimed = 0
        # new_running_tasks = []
        if time in self.pending:
            for task in self.pending[time]:
                # task.execute()
                # if task.isFinished():
                self.acc_cost += self.cost(task)
                reclaimed += task.resource
                task.status = rm.Status.FINISHED
                task.finish_time = time
                task.workload.finished_tasks.append(task)
                    #finished.append(task)
                # else:
                    # new_running_tasks.append(task)
        # self.running_tasks = new_running_tasks
        # reclaim additional resources when done running tasks
        #if reclaimed > 0:
        #    self.free_capacity += reclaimed
        #    if self.shrink_capacity > 0:
        #        self.reclaim(0)
        if self.shrink_capacity < reclaimed:
            self.free_capacity += reclaimed - self.shrink_capacity
            self.shrink_capacity = 0
        else:
            self.shrink_capacity -= reclaimed
        return

    def cost(self, task):
        # cost = resource * runtime * cost_per_resource
        # duration is max of min duration for the pool and task duration
        # assuming cost per resource is 1
        return task.resource * max(task.runtime, self.od_min_len)
