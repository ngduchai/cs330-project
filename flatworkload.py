
import rm;

class FlatWorkload(rm.Workload):
    def __init__(self, load, task_size, value_per_slot, poolname):
        rm.Workload.__init__(self)
        self.load = load
        self.value_per_slot = float(value_per_slot)
        self.id_count = 0
        self.poolname = poolname
        self.task_size = task_size
        self.failed_tasks = []
 
    def make_request(self):
        tasks = self.failed_tasks;
        self.failed_tasks = [];
        resource = 0;
        while resource < self.load:
            tasks.append(rm.Task(self.id_count, 0, self.task_size, 1, self.poolname, self))
            resource += self.task_size
            self.id_count += 1
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
            value += self.value_per_slot * float(task.resource) / self.load / (task.finish_time - task.arrival_time)
        return value



