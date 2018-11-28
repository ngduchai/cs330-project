
import rm;

class StaticRM(rm.RM):
    def __init__(self, capacity):
        rm.RM.__init__(self, capacity)
        self.free_resource = capacity

    def adjust_partition(self):
        if self.free_resource > 0:
            total_weight = 0;
            for pool in self.pools:
                total_weight += pool.weight
            for pool in self.pools:
                pool.alloc(self.free_resource * pool.weight / total_weight)
            self.free_resource = 0



