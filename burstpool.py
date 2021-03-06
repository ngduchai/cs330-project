import rm
import math

class BurstPool(rm.Pool):
    def __init__(self, weight, task_guarantee, inv_cost):
        rm.Pool.__init__(self, weight)
        self.runtime_limit = 16200
        self.inv_cost = inv_cost
        self.run_length = []
        self.task_guarantee = task_guarantee#number of task
        self.max_resource = 5#number of maximum resource for each task
        self.time_guarantee = 30#time frames for the guarantee
        self.requirement = self.task_guarantee*self.max_resource*(self.runtime_limit/self.time_guarantee)
        self.counter = [0]*2
        self.pending = {}
        self.acc_cost = 0
        # self.shrink_capacity = 0

    def extra_capacity(self):
        #return the number of resources can be reclaimed or extra number of resources can give to tasks         
        if self.capacity <= self.requirement:
            return 0
        else:
            unit_resource = 0
            if self.run_length:
                unit_resource = math.ceil(max(self.run_length)/self.time_guarantee)*self.max_resource*self.task_guarantee
            return (self.capacity-self.requirement-max(self.capacity-self.free_capacity-unit_resource, 0))

    def reclaim(self, unit):
        #reclaim resources
        self.shrink_capacity += unit
        if self.capacity <= self.requirement:
            return 0
        else:
            temp = min(self.extra_capacity(), self.shrink_capacity)
            self.capacity -= temp
            self.shrink_capacity -= temp
            self.free_capacity -= temp
            return temp

    def launch_task(self, time, tasks):
        finished = []
        #add new tasks from input to the running_tasks list
        self.counter[0] += 1
        max_launch = self.extra_capacity()+self.task_guarantee*self.max_resource-self.counter[1]
        #for task in tasks:
        for i in range(len(tasks)):
            task = tasks[i]
            #launch if there's enough resource
            if task.resource <= self.max_resource and task.resource <= max_launch and task.resource <= self.free_capacity:
                self.free_capacity -= task.resource
                self.counter[1] += task.resource

                task.status = rm.Status.RUNNING

                #self.running_tasks.append(task)
                #self.run_length.append(0)

                finish_time = time + min(task.runtime, self.runtime_limit)
                if finish_time not in self.pending:
                    self.pending[finish_time] = []
                self.pending[finish_time].append(task)

            #else reject
            else:
                #task.status = rm.STATUS_FAILED
                #finished.append(task)
                # We break the interface to improve the implementation here
                if hasattr(task.workload, 'failed_burst_tasks'):
                    task.workload.failed_burst_tasks += tasks[i:]
                else:
                    task.workload.failed_tasks += tasks[i:]
                break;
        # print time
        # execute running tasks
        #i = 0
        #print len(self.running_tasks)
        #while i < len(self.running_tasks):
        #    task = self.running_tasks[i]
        #    task.execute()
        #    self.run_length[i] += 1
            #remove if it's finished
        #    if task.isFinished():
        #        self.free_capacity += task.resource
                # task.status = rm.Status.FINISHed
                #finished.append(task)

        #        task.finish_time = time + 1
        #        task.workload.finished_tasks.append(task)
        #        self.running_tasks.pop(i)
        #        self.run_length.pop(i)
            #remove if it runs over max_time_length
        #    elif self.run_length[i] >= self.runtime_limit:
        #        self.free_capacity += task.resource
                # task.status = rm.STATUS_KILLED
                #finished.append(task)

        #        if hasattr(task.workload, 'failed_burst_tasks'):
        #           task.workload.failed_burst_tasks.append(task)
        #        else:
        #           task.workload.failed_tasks.append(task)
        #        
        #        self.running_tasks.pop(i)
        #        self.run_length.pop(i)
        #    else:
        #        i += 1
        # print time
        if time in self.pending:
            for task in self.pending[time]:
                # print "finish burst"
                self.free_capacity += task.resource
                self.acc_cost += self.cost(task)
                if task.runtime <= self.runtime_limit:
                    task.status = rm.Status.FINISHED
                
                    task.finish_time = time
                    task.workload.finished_tasks.append(task)
                else:
                    task.status = rm.Status.KILLED
                    task.finish_time = time
                    if hasattr(task.workload, 'failed_burst_tasks'):
                        task.workload.failed_burst_tasks.append(task)
                    else:
                        task.workload.failed_tasks.append(task)

        if self.counter[0] >= self.time_guarantee:
            self.counter = [0]*2
        self.reclaim(0)
        #return finished
        return

    def cost(self, task):
        # cost = resource * runtime * cost_per_resource
        # duration is max of min duration for the pool and task duration
        # assuming cost per resource is 1
        return self.inv_cost + task.resource * min(task.runtime, self.runtime_limit) * 0.8
