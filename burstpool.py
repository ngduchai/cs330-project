import rm

class BurstPool(rm.Pool):
    def __init__(self, weight, limit, inv_cost):
        rm.Pool.__init__(self, weight)
        self.runtime_limit = limit
        self.inv_cost = inv_cost
        self.run_length = []
        self.task_guarantee = 1#number of task
        self.max_resource = 5#number of maximum resource for each task
        self.time_guarantee = 1#time frames for the guarantee
        self.requirement = self.task_guarantee*self.max_resource*(limit/self.time_guarantee)#minimum requirement for guarantees
        # self.shrink_capacity = 0

    def extra_capacity(self):
        #return the number of resources can be reclaimed or extra number of resources can give to tasks         
        if self.capacity <= self.requirement:
            return 0
        else:
            unit_resource = max(self.run_length)/self.time_guarantee*self.max_resource*self.task_guarantee
            return (self.capacity-self.requirement-max(self.capacity-self.free_capacity-unit_resource, 0))

    def reclaim(self, unit):
        #reclaim resources
        self.shrink_capacity += unit
        if self.capacity <= self.requirement:
            return 0
        else:
            temp = min(self.extra_capacity(), self.shrink_capacity)
            self.capacity -= temp
            self.shrink_capacity -= temp
            self.free_capacity -= temp
            return temp

    def launch_task(self, tasks):
        finished = []
        #add new tasks from input to the running_tasks list
        max_launch = self.extra_capacity()+self.task_guarantee*self.max_resource
        for task in tasks:
            #launch if there's enough resource
            if task.resource <= self.max_resource and task.resource <= max_launch and self.free_capacity >= task.resource:
                self.free_capacity -= task.resource
                max_launch -= task.resource
                task.status = rm.STATUS_RUNNING
                self.running_tasks.append(task)
                self.run_length.append(0)
            #else reject
            else:
                task.status = rm.STATUS_FAILED
                finished.append(task)
        # execute running tasks
        i = 0
        while i < len(self.running_tasks):
            task = self.running_tasks[i]
            task.execute()
            self.run_length[i] += 1
            #remove if it's finished
            if task.isFinished():
                self.free_capacity += task.resource
                task.status = rm.STATUS_FINISH
                finished.append(task)
                self.running_tasks.pop(i)
                self.run_length.pop(i)
            #remove if it runs over max_time_length
            elif self.run_length[i] >= self.runtime_limit:
                self.free_capacity += task.resource
                task.status = rm.STATUS_KILLED
                finished.append(task)
                self.running_tasks.pop(i)
                self.run_length.pop(i)
            else:
                i += 1
        self.reclaim(0)
        return finished

    def cost(self, task):
        # cost = resource * runtime * cost_per_resource
        # duration is max of min duration for the pool and task duration
        # assuming cost per resource is 1
        if task.status == rm.STATUS_FINISH:
            return inv_cost + task.resource * min(task.runtime, self.runtime_limit) * 0.8
        else:
            return 0