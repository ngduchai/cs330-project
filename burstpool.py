import rm

class BurstPool(rm.Pool):
    def __init__(self, *args, **kwargs):
        super(BurstPool, self).__init__(*args, **kwargs)
        # self.shrink_capacity = 0

    def reclaim(self, unit):
        #reclaim resources
        self.shrink_capacity += unit
        if self.free_capacity >= self.shrink_capacity:
            unit = self.shrink_capacity
            self.free_capacity -= unit
            # self.capacity -= unit
            self.shrink_capacity = 0
            return unit
        else:
            temp = self.free_capacity
            # self.capacity -= temp
            self.shrink_capacity -= temp
            self.free_capacity = 0
            return temp

    def launch_task(self, tasks):
        # run each task
        finished = []
        for task in tasks:
            task.execute()
            if task.isFinished():
                self.free_capacity += task.resource
                finished.append(task)
        if self.shrink_capacity > 0 and self.free_capacity > 0:
            self.reclaim(0)
        return finished

    def cost(self, task):
        # cost = resource * runtime * cost_per_resource
        # duration is max of min duration for the pool and task duration
        # assuming cost per resource is 1
        return task.resource * task.runtime
