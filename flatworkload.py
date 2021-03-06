
import rm;

class FlatWorkload(rm.Workload):
    def __init__(self, load, task_size, value_per_unit, poolname):
        rm.Workload.__init__(self)
        self.load = load
        self.value_per_unit = float(value_per_unit)
        self.id_count = 0
        self.poolname = poolname
        self.task_size = task_size
        self.failed_tasks = []
 
    def make_request(self, time, pools):
        if self.poolname not in pools:
            pools[self.poolname] = []
        #pools[self.poolname] += self.failed_tasks; # resubmit all failed tasks
        #self.failed_tasks = []
        resource = 0;
        while resource < self.load:
            pools[self.poolname].append(rm.Task(self.id_count, time,
                self.task_size, 1, self.poolname, self))
            resource += self.task_size
            self.id_count += 1
        return

    def update(self, tasks):
        for task in tasks:
            if (task.status == rm.Status.FINISHED):
                self.finished_tasks.append(task)
            #if (task.status != rm.Status.FINISHED):
            #    self.failed_tasks.append(task)
            #else:
            #    self.finished_tasks.append(task);

    def value(self):
        value = 0
        for task in self.finished_tasks:
            value += self.value_per_unit * float(task.resource) / (task.finish_time - task.arrival_time)
        return value



