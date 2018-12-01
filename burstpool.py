import rm

class BurstPool(rm.Pool):
    def __init__(self, *args, **kwargs):
        super(BurstPool, self).__init__(*args, **kwargs)
        # self.shrink_capacity = 0
、        self.od_min_len = od_min_len

    def reclaim(self, unit):
        #reclaim resources
        if self.free_capacity >= unit:
            self.free_capacity -= unit
            self.capacity -= unit
            return unit
        else:
            temp = self.free_capacity
            self.capacity -= temp
            self.shrink_capacity += (unit-temp)
            self.free_capacity = 0
            return temp

    def launch_task(self, tasks):
        # run each task
        reclaimed = 0
        finished = []
        for task in tasks:
            task.execute()
            if task.isFinished():
                reclaimed += task.resource
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
        return task.resource * task.runtime
