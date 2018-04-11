from KMCLib import *
from time import time as timer
import os

class TimeBreaker(KMCBreakerPlugin):

    def __init__(self, length):
        self.length = length   # actual time length, s

    def setup(self, step, time, configuration):
        self.start = timer()

    def evaluate(self, step, time, configuration):
        if timer() - self.start > self.length:
            return True
        else:
            return False


class FileBreaker(KMCBreakerPlugin):

    def __init__(self, file_name):
        self.file_name = file_name

    def evaluate(self, step, time, configuration):
        if os.path.exists(self.file_name):
            return True
        else:
            return False
