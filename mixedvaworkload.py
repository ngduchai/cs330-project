
import rm;
import random;

import numpy as np

class MixedVAWorkload(rm.Workload):
    def __init__(self, ratio, lamb, value_per_slot, normal_load,
            burst_height, burst_width, timeliness, task_size, ondemand, burst):
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
        self.failed_burst_tasks = []
        self.failed_ondemand_tasks = []
        self.setup_burst_time = []
        self.burst_time = []
        self.ratio = ratio
        self.ondemand = ondemand
        self.burst = burst
        self.mean_runtime = 5 * 60 * 30
        self.stddev_runtime = 2 * 60 * 30

    def setup(self, time):
        t = 0
        while t < time:
            bt = int(random.expovariate(self.lamb))
            t += bt
            self.setup_burst_time.append(bt)

    def restart(self):
        self.bursts = []
        self.id_count = 0
        self.failed_burst_tasks = []
        self.failed_ondemand_tasks = []
        self.wait_for_burst = self.setup_burst_time[0]
        self.burst_time = []
        for i in range(len(self.setup_burst_time) - 1):
            self.burst_time.append(self.setup_burst_time[i+1])
        self.finished_tasks = []

    def make_request(self, time, pools):

        if self.ondemand not in pools:
            pools[self.ondemand] = []
        pools[self.ondemand] += self.failed_ondemand_tasks; # resubmit all failed tasks
        self.failed_ondemand_tasks = []
        if self.burst not in pools:
            pools[self.burst] = []
        pools[self.burst] += self.failed_burst_tasks; # resubmit all failed tasks
        self.failed_burst_tasks = []
        # submit new tasks
        if self.wait_for_burst != 0:
            t = rm.Task(self.id_count, time, self.normal_load, 1, self.ondemand, self)
            self.id_count += 1
            pools[self.ondemand].append(t)
            self.wait_for_burst -= 1
        else:
            if len(self.burst_time) > 0:
                self.wait_for_burst = self.burst_time.pop()
            else:
                self.wait_for_burst = int(random.expovariate(self.lamb))
            self.bursts.append(self.burst_width)
        
        # generating bursts
        new_bursts = []
        for burst in self.bursts:
            ondemand_height = self.ratio * self.burst_height
            burst_height = self.burst_height - ondemand_height
            resource = 0
            while resource < ondemand_height:
                length = int(np.random.normal(self.mean_runtime, self.stddev_runtime))
                t = rm.Task(self.id_count, time, self.task_size, length, self.ondemand, self)
                pools[self.ondemand].append(t)
                self.id_count += 1
                resource += self.task_size
            
            resource = 0
            while resource < burst_height:
                length = int(np.random.normal(self.mean_runtime, self.stddev_runtime))
                t = rm.Task(self.id_count, time, self.task_size, length, self.burst, self)
                pools[self.burst].append(t)
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



