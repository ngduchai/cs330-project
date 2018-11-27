
import math;

class Task:
    def __init__(self, id, computation_unit, expected_exec_time, arrival_time):
        # Task id, should be globally unique
        self.id = id
        # Computation needed per time unit
        self.computation_unit = computation_unit
        # Expected execution time
        self.expected_exec_time = expected_exec_time
        # Arrival time
        self.arrival_time = arrival_time
        # Finish time, = -1 means the task havnt done yet
        self.finish_time = -1
        # Actually execution time
        self.exec_time = 0
        # if work<= 0 then the task finishes 
        self.work = self.expected_exec_time * self.computation_unit
        # Actually resourcea assigned to the task
        self.assigned_unit = 0
        # 


    def has_done():
        return finish_time != -1

    
    def make_progress(start_time, length):
        # Run task at 'start_time' for a length of 'length'
        progress = length * self.assigned_unit
        if (self.work < progress):
            progress = math.ceil(self.work / self.assigned_unit)
            self.work = 0
            self.finish_time = start_time + progress
        else:
            self.work -= progress

        self.exec_time += progress;


