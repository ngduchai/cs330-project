
import rm;
import random;

class VAWorkload(rm.Workload):
    def __init__(self, lamb, value_per_slot, normal_load,
            burst_height, burst_width, timeliness, task_size, poolname):
        rm.Workload.__init__(self)
        self.lamb = lamb
        self.value_per_slot = float(value_per_slot)
        self.burst_height = burst_height
        self.burst_width = burst_width
        self.timeliness = timeliness
        self.normal_load = normal_load
        self.bursts = []
        self.wait_for_burst = int(random.expovariate(self.lamb))
        self.id_count = 0
        self.task_size = task_size
        self.poolname = poolname
        self.failed_tasks = []
 
    def make_request(self):
        tasks = self.failed_tasks; # resubmit all failed tasks
        self.failed_tasks = []
        if self.wait_for_burst != 0:
            t = rm.Task(self.id_count, 0, self.normal_load, 1, self.poolname, self)
            self.id_count += 1
            tasks.append(t)
            self.wait_for_burst -= 1
        else:
            self.wait_for_burst = int(random.expovariate(self.lamb))
            self.bursts.append(self.burst_width)
        
        new_bursts = []
        for burst in self.bursts:
            resource = 0
            while resource < self.burst_height:
                tasks.append(rm.Task(self.id_count, 0, self.task_size, 1, self.poolname, self))
                self.id_count += 1
                resource += self.task_size
            burst -= 1
            if burst != 0:
                new_bursts.append(burst)
        self.bursts = new_bursts
        return tasks

    def update(self, tasks):
        for task in tasks:
            if (task.status != rm.Status.FINISHED):
                self.failed_tasks.append(task)
            else:
                self.finished_tasks.append(task);

    def value(self):
        value = 0
        for task in self.finished_tasks:
            if task.resource != self.normal_load:
                # Only burst generates value
                latency = task.finish_time - task.arrival_time
                value += self.value_per_slot * (self.timeliness ** (-latency))
        return value



