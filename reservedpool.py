import rm

class ReservedPool(rm.Pool):
    def __init__(self, weight):
        rm.Pool.__init__(self, weight)
        self.shrink_capacity = 0

    def reclaim(self, unit):
        # just ignore
        return 0

    def launch_task(self, tasks):
        # Waiting queue is a FIFO queue, we first add new task to the waiting queue then check
        # try to running the very first tasks
        for task in tasks:
            self.waiting_queue.append(task)
        # Launch new task
        while len(self.waiting_queue) > 0:
            if self.waiting_queue[0].resource <= self.free_capacity:
                task = self.waiting_queue.pop()
                self.free_capacity -= task.resource
                self.running_tasks.append(task)
            else:
                break
        
        # Execute task and collect finished tasks
        finished_tasks = []
        new_running_tasks = []
        for task in self.running_tasks:
            task.execute()
            if task.remained_work <= 0:
                self.free_capacity += task.resource
                finished_tasks.append(task)
            else:
                new_running_tasks.append(task)
        self.running_tasks = new_running_tasks
        return finished_tasks
        

