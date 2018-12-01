import rm

class OnDemandPool(rm.Pool):
    def __init__(self, od_min_len, *args, **kwargs):
        super(OnDemandPool, self).__init__(*args, **kwargs)
        # self.shrink_capacity = 0
        self.shrink_left = 0
        self.od_min_len = od_min_len

    def reclaim(self, unit):
        #reclaim resources
        #add unit to amount to be reclaimed shrink as much as possible
        self.shrink_left += unit
        if self.shrink_capacity >= self.shrink_left:
            # shrink by all of shrink_left
            self.shrink_capacity -= self.shrink_left
            self.shrink_left = 0
            return unit
        else:
            # shrink by shrink_capacity
            shrink_amt = self.shrink_capacity
            self.shrink_left -= shrink_amt
            self.shrink_capacity = 0
            return shrink_amt

    def launch_task(self, tasks):
        # add the task to running_task if enough resources, or reject
        finished = []
        for task in tasks:
            if task.resource <= self.free_capacity:
                self.free_capacity -= task.resource
                self.running_tasks.append(task)
            else:
                task.status = rm.Status.REJECTED
                finished.append(task)

        # run each task
        reclaimed = 0
        for task in self.running_tasks:
            task.execute()
            if task.isFinished():
                reclaimed += task.resource
                task.status = rm.Status.FINISHED
                finished.append(task)
       
        # reclaim additional resources when done running tasks
        if self.shrink_left > 0:
            self.shrink_capacity += reclaimed
            self.reclaim(0)
        return finished

    def cost(self, task):
        # cost = resource * runtime * cost_per_resource
        # duration is max of min duration for the pool and task duration
        # assuming cost per resource is 1
        return task.resource * max(task.runtime, self.od_min_len)
