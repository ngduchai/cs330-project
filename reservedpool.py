import rm

class ReservedPool(Pool):
    def __init__(self, weight):
        super().__init__(weight)
        self.shrink_pending = 0

    def reclaim(self, unit):
        if unit >= self.free_capacity:
            # if there are enough resource, then shrink the capacity by unit
            self.capacity -= unit
            self.free_capacity -= unit
        else:
            # if there is not enough resource, then return all free resource and pend the rest
            self.capacity -= self.free_capacity
            self.shrink_pending = unit - self.free_capacity
            self.free_capacity = 0

    def launch_task(self, tasks):
        # Waiting queue is a FIFO queue, we first add new task to the waiting queue then check
        # try to running the very first tasks
        for task in tasks:
            self.waiting_queue.append(task)
        
        # Launch new task
        while self.waiting_queue.count > 0:
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
            if task.remained_work == 0:
                finished_tasks.append(task)
            else:
                new_running_tasks.append(task)
        self.running_tasks = new_running_tasks
        return finished_tasks
        

