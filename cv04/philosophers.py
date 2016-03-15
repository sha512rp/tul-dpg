

from threading import Condition
import time


class Fork:

    def __init__(self):
        self.condition = Condition()
        self.being_used = False

    def use(self, delay):
        with self.condition:
            self.condition.wait_for(self.can_use)
            self.being_used = True
            time.sleep(delay)
            self.being_used = False
            self.notify()

    def can_use(self):
        return not self.being_used


class Philosopher:
    """Can access two adjacent forks, either thinks or wants to eat.
       Eating requires access to both forks.
    """
    pass