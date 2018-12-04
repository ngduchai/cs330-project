import unittest

import sys
sys.path.insert(0, './..')

from rm import Task, Status
from ondemandpool import OnDemandPool

class TestOnDemandPool(unittest.TestCase):

    def test_reclaim_all(self):
        # test reclaiming when there is more than enough capacity
        CAPACITY = 5
        TRY_RECLAIM = 3
        pool = OnDemandPool(None, None)
        pool.free_capacity = CAPACITY
        reclaimed = pool.reclaim(TRY_RECLAIM)
        self.assertEqual(reclaimed, TRY_RECLAIM)
        self.assertEqual(pool.free_capacity, CAPACITY - TRY_RECLAIM)
        self.assertEqual(pool.shrink_capacity, 0)

    def test_reclaim_part(self):
        # test reclaiming when there is not enough capacity
        CAPACITY = 3
        TRY_RECLAIM = 5
        pool = OnDemandPool(None, None)
        pool.free_capacity = CAPACITY
        reclaimed = pool.reclaim(TRY_RECLAIM)
        self.assertEqual(reclaimed, CAPACITY)
        self.assertEqual(pool.free_capacity, 0)
        self.assertEqual(pool.shrink_capacity, TRY_RECLAIM - CAPACITY)

    def test_launch_task_and_reclaim(self):
        # test launch_task when a task finishes and frees resources
        SHRINK_CAPACITY = 5
        pool = OnDemandPool(None, None)
        pool.shrink_capacity = SHRINK_CAPACITY
        TASK_RESOURCE = 2
        TASK_RUNTIME = 1
        FREE_CAPACITY = 2
        task = Task(None, None, TASK_RESOURCE, TASK_RUNTIME, None, None)
        self.assertEqual(task.remained_work, task.resource)
        tasks = [task]
        pool.free_capacity = FREE_CAPACITY
        finished = pool.launch_task(tasks)
        self.assertEqual(finished, tasks)
        self.assertEqual(pool.shrink_capacity, SHRINK_CAPACITY - task.resource)
        self.assertEqual(task.status, Status.FINISHED)

    def test_launch_task_reject(self):
        # test rejecting a task
        SHRINK_CAPACITY = 5
        pool = OnDemandPool(None, None)
        pool.shrink_capacity = SHRINK_CAPACITY
        TASK_RESOURCE = 5
        TASK_RUNTIME = 1
        FREE_CAPACITY = 2
        task = Task(None, None, TASK_RESOURCE, TASK_RUNTIME, None, None)
        self.assertEqual(task.remained_work, task.resource)
        tasks = [task]
        pool.free_capacity = FREE_CAPACITY
        finished = pool.launch_task(tasks)
        self.assertEqual(pool.shrink_capacity, SHRINK_CAPACITY)
        self.assertEqual(task.status, Status.REJECTED)
             

    def test_cost_long_task(self):
        # test cost for runtime longer than min
        TASK_RUNTIME = 80
        TASK_RESOURCE = 15
        OD_MIN_LEN = 12
        pool = OnDemandPool(OD_MIN_LEN, None)
        task = Task(None, None, TASK_RESOURCE, TASK_RUNTIME, None, None)
        cost = pool.cost(task)
        self.assertEqual(cost, TASK_RUNTIME * TASK_RESOURCE)

    def test_cost_short_task(self):
        # test cost for runtime shorter than min
        TASK_RUNTIME = 10
        TASK_RESOURCE = 15
        OD_MIN_LEN = 12
        pool = OnDemandPool(OD_MIN_LEN, None)
        task = Task(None, None, TASK_RESOURCE, TASK_RUNTIME, None, None)
        cost = pool.cost(task)
        self.assertEqual(cost, OD_MIN_LEN * TASK_RESOURCE) 
        
    def test_task_submission(self):
        pool = OnDemandPool(None, None)
        pool.alloc(100)
        # continously submitting tasks with 1 resource and last for 1 timeslot
        # since the pool capacity is 100, no task would be rejected
        for i in range(1000):
            task = Task(None, None, 1, 1, None, None)
            finished_tasks = pool.launch_task([task])
            for task in finished_tasks:
                self.assertEqual(task.status, Status.FINISHED)

if __name__ == '__main__':
    unittest.main()
