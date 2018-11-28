import rm

class ReservedPool(rm.Pool):
    def __init__(self, weight):
        rm.Pool.__init__(self, weight)
        self.shrink_pending = 0

    def reclaim(self, unit):
        if unit >= self.free_capacity:
            # if there are enough resource, then shrink the capacity by unit
            self.capacity -= unit
            self.free_capacity -= unit
            return unit
        else:
            # if there is not enough resource, then return all free resource and pend the rest
            self.capacity -= self.free_capacity
            self.shrink_pending = unit - self.free_capacity
            self.free_capacity = 0
            return unit - self.shrink_pending

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
                # task finish, pool reclaim resource, but first it should check if there are
                # resource it need to return to resource manager.
                if self.shrink_pending > 0:
                    # if there is, then freed resources are return to resource manager instead
                    if self.shrink_pending <= task.resource:
                        self.capacity -= self.shrink_pending
                        self.free_capacity += task.resource - self.shrink_pending
                        self.shrink_pending = 0
                    else:
                        self.shrink_pending -= task.resource
                else:
                    # otherwise, return free resource to the pool
                    self.free_capacity += task.resource

                finished_tasks.append(task)
            else:
                new_running_tasks.append(task)
        self.running_tasks = new_running_tasks
        return finished_tasks
        

