import math;

class RM:
    def __init__(self, capacity, ):
        #set the capacity of all resourcews
        self.capacity = capacity
        self.pools = []

    def add_pool(self, pool):
        #add one pool      
        self.pools.append(pool)

    def adjust_partition(self):
    # if static, doesn't change; if dynamic, re-adjusting the partition between pools


class Pool:
    def __init__(self, weight):
        #set the capacity of all resourcews
        self.capacity = 0
        self.weight = weight
        self.free_capacity = self.capacity
        self.task_queue = []
        #need to keep track of tasks

    def alloc(self, capacity):
        #allocate new resources     
        self.capacity += capacity

    def reclaim(self, unit):
    	#reclaim resources
    	#Check the task before returning resources to the manager

    def launch_task(self, tasks):
    	
    	#launch specific task on a set of resources

    def task_finished(self):
    	#return a list of tasks that have finished at this particular time slot

    def cost(self, task):
    	return None
    	#???  Calculate the cost for one task ???
class Task:
    def __init__(self, id, arrival_time, resource, runtime):
    	self.id = id
    	self.arrival_time = arrival_time
    	self.resource = resource #required resource size
    	self.finish_time = -1
    	self.remained_work = resource*runtime
    	self.runtime = runtime


    def add_pool(self, pool):

    def execute(self):

class Workload:
    def __init__(self):
        #set the capacity of all resourcews
        self.finished_tasks = []


    def make_request(self):
        #create a list of tasks and submit it to pool        

    def update(self, tasks):# tasks = a list of finished tasks

    def value(self):