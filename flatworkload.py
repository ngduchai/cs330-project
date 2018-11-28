
import rm;

class FlatWorkload(Workload):
    def __init__(self, load, value_per_slot):
        super().__init__()
        self.load = load
        self.value_per_slot = value_per_slot
        self.id_count = 0
 
    def make_request(self):
        Task t(id_count, 0, load, 1, POOL_RESERVED, self)
        id_count += 1
        return [t]

    def update(self, tasks):
        for task in tasks:
            self.finished_tasks.append(task);

    def value(self):
        value = 0
        for task in finished_tasks:
            value += value_per_slot / (task.finished_tasks - task.arrival_time)
        return value



