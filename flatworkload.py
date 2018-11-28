
import rm;

class FlatWorkload(rm.Workload):
    def __init__(self, load, value_per_slot):
        rm.Workload.__init__(self)
        self.load = load
        self.value_per_slot = value_per_slot
        self.id_count = 0
 
    def make_request(self):
        t = rm.Task(self.id_count, 0, self.load, 1, rm.POOL_RESERVED, self)
        self.id_count += 1
        return [t]

    def update(self, tasks):
        for task in tasks:
            self.finished_tasks.append(task);

    def value(self):
        value = 0
        for task in self.finished_tasks:
            value += self.value_per_slot / (task.finish_time - task.arrival_time)
        return value



