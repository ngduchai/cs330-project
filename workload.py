


class Workload:

    def __init__(self, name):
        self.name = name;
        self.count = 0;
        self.running_tasks = {};
        self.finished_tasks = {};
        self.failed_tasks = {};

    def consume(t):
        # Return resource need by the workload at time t
        self.count += 1;
        id = name + "-" + str(self.count)
        task = Task(id, 10, 10, t)
        self.running_tasks[id] = task
        return task, "on-demand"

    def finish(task, t):
        # Let the workload know that the time t, a task has
        # been terminated (either successfully or failed)
        if (task.id in self.running_tasks):
            self.





