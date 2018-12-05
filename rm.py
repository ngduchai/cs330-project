import math;
from enum import Enum

# Define pool names
POOL_RESERVED = 'reserved' # only for testing purpose
POOL_ON_DEMAND = 'on-demand'
POOL_BURST = 'burst'
POOL_VOLATILE = 'volatile'

class Status(Enum):
    FINISHED = 0
    REJECTED = 1
    WAITING = 2
    RUNNING = 3
    KIILED = 4

class RM:
    def __init__(self, capacity):
        #set the capacity of all resourcews
        self.capacity = capacity
        self.pools = []

    def add_pool(self, pool):
        #add one pool      
        self.pools.append(pool)

    def adjust_partition(self):
    # if static, doesn't change; if dynamic, re-adjusting the partition between pools
        return

class Pool(object):
    def __init__(self, weight):
        #set the capacity of all resourcews
        self.capacity = 0
        self.weight = weight
        self.free_capacity = self.capacity
        self.shrink_capacity = 0
        self.waiting_queue = []
        self.running_tasks = []
        #need to keep track of tasks

    def alloc(self, capacity):
        #allocate new resources     
        self.capacity += capacity
        self.free_capacity += capacity

    def reclaim(self, unit):
    	#reclaim resources
    	#Check the task before returning resources to the manager
        return

    def launch_task(self, time, tasks):
    	#call task.execute() every time
    	#launch specific task on a set of resources
        #return a list of tasks that have finished at this particular time slot 
        return

    # def task_finished(self):
    # 	#return a list of tasks that have finished at this particular time slot

    def cost(self, task):
    	return None
    	#???  Calculate the cost for one task ???

class Task:
    def __init__(self, task_id, arrival_time, resource, runtime, pool, workload):
        self.id = task_id
        self.arrival_time = arrival_time
        self.resource = resource #required resource size
        self.finish_time = -1
        self.remained_work = resource*runtime
        self.runtime = runtime
        self.pool = pool
        self.workload = workload
        self.status = Status.WAITING

    def execute(self):
        #update the self.remained_work
        self.remained_work -= self.resource

    def isFinished(self):
        return self.remained_work == 0

class Workload:
    def __init__(self):
        #set the capacity of all resourcews
        self.finished_tasks = []


    def make_request(self, time, pools):
        #create a list of tasks and submit it to pool        
        return

    def update(self, tasks):# tasks = a list of finished tasks
        return

    def value(self):
        return

