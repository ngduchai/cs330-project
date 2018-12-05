
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
        self.setup_burst_time = []
        self.burst_time = []

    def setup(self, time):
        t = 0
        while t < time:
            bt = int(random.expovariate(self.lamb))
            t += bt
            self.setup_burst_time.append(bt)

    def restart(self):
        self.bursts = []
        self.id_count = 0
        self.failed_tasks = []
        self.wait_for_burst = self.setup_burst_time[0]
        self.burst_time = []
        for i in range(len(self.setup_burst_time) - 1):
            self.burst_time.append(self.setup_burst_time[i+1])
        self.finished_tasks = []

    def make_request(self, time, pools):
        if self.poolname not in pools:
            pools[self.poolname] = []
        pools[self.poolname] += self.failed_tasks; # resubmit all failed tasks
        self.failed_tasks = []
        if self.wait_for_burst != 0:
            t = rm.Task(self.id_count, time, self.normal_load, 1, self.poolname, self)
            self.id_count += 1
            pools[self.poolname].append(t)
            self.wait_for_burst -= 1
        else:
            if len(self.burst_time) > 0:
                self.wait_for_burst = self.burst_time.pop()
            else:
                self.wait_for_burst = int(random.expovariate(self.lamb))
            self.bursts.append(self.burst_width)
        
        new_bursts = []
        for burst in self.bursts:
            resource = 0
            while resource < self.burst_height:
                t = rm.Task(self.id_count, time, self.task_size, 1, self.poolname, self)
                pools[self.poolname].append(t)
                self.id_count += 1
                resource += self.task_size
            burst -= 1
            if burst != 0:
                new_bursts.append(burst)
        self.bursts = new_bursts
        return

    def update(self, tasks):
        for task in tasks:
            if (task.status != rm.Status.FINISHED):
                self.failed_tasks.append(task)
            else:
                self.finished_tasks.append(task);

    def value(self):
        value = 0
        raw_value = float(self.value_per_slot) * self.task_size / self.burst_height
        for task in self.finished_tasks:
            if task.resource != self.normal_load:
                # Only burst generates value
                latency = task.finish_time - task.arrival_time
                value += raw_value * (self.timeliness ** (-latency))
        return value



