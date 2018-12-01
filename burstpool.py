import rm

class BurstPool(rm.Pool):
    def __init__(self, limit, inv_cost):
        rm.Pool.__init__(self, weight)
        self.runtime_limit = limit
        self.inv_cost = inv_cost
        self.run_length = []
        # self.shrink_capacity = 0

    def reclaim(self, unit):
        #reclaim resources
        self.shrink_capacity += unit
        if self.free_capacity >= self.shrink_capacity:
            unit = self.shrink_capacity
            self.free_capacity -= unit
            self.capacity -= unit
            self.shrink_capacity = 0
            return unit
        else:
            temp = self.free_capacity
            self.capacity -= temp
            self.shrink_capacity -= temp
            self.free_capacity = 0
            return temp

    def launch_task(self, tasks):
        finished = []
        #add new tasks from input to the running_tasks list
        for task in tasks:
            #launch if there's enough resource
            if self.free_capacity >= task.resource:
                free_capacity -= task.resource
                task.status = STATUS_RUNNING
                self.running_tasks.append(task)
                self.run_length.append(0)
            #else reject
            else:
                task.status = STATUS_FAILED
                finished.append(task)
        # execute running tasks
        for i in range(len(self.running_tasks)):
            task = self.running_tasks[i]
            task.execute()
            self.run_length[i] += 1
            #remove if it's finished
            if task.isFinished():
                self.free_capacity += task.resource
                task.status = STATUS_FINISH
                finished.append(task)
                self.running_tasks.pop(i)
                self.run_length.pop(i)
            #remove if it runs over max_time_length
            elif self.run_length[i] >= self.running_limit:
                self.free_capacity += task.resource
                task.status = STATUS_KILLED
                finished.append(task)
                self.running_tasks.pop(i)
                self.run_length.pop(i)
        if self.shrink_capacity > 0 and self.free_capacity > 0:
            self.reclaim(0)
        return finished

    def cost(self, task):
        # cost = resource * runtime * cost_per_resource
        # duration is max of min duration for the pool and task duration
        # assuming cost per resource is 1
        return inv_cost + task.resource * min(task.runtime, self.running_limit) * 0.8
