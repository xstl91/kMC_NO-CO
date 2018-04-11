from KMCLib import *
from .routine import processes
from __main__ import end_list

class Breaker(KMCBreakerPlugin):

    def __init__(self):
        self.breaker = { i:(p.name[0],p.name[2]) for i,p in enumerate(processes) if p.name[0] in end_list }

    def evaluate(self, step, time, configuration):
        if configuration.latestEventProcess() in self.breaker:
            self.end_time = time
            self.end_process = self.breaker[ configuration.latestEventProcess() ]
            return True
        else:
            return False
