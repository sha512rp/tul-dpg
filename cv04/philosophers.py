

from threading import Condition, Thread
import time
import random


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
            self.condition.notify()

    def can_use(self):
        return not self.being_used


class Philosopher(Thread):
    """Can access two adjacent forks, either thinks or wants to eat.
       Eating requires access to both forks.
    """

    EATING_TIME = 0.5

    def __init__(self, left_fork, right_fork, name):
        super(Philosopher, self).__init__()
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.name = name
        self.just_ate = False

    def can_eat(self):
        return not self.just_ate and self.left_fork.can_use() and self.right_fork.can_use()

    def eat(self):
        print("{:s}: Eating".format(self.name))
        self.left_fork.use(Philosopher.EATING_TIME)
        self.right_fork.use(Philosopher.EATING_TIME)
        self.just_ate = True
        print("{:s}: Done Eating".format(self.name))

    def think(self):
        print("{:s}: Thinking".format(self.name))
        time.sleep(random.random())
        self.just_ate = False

    def run(self):
        while True:
            print("{:s} Deciding...".format(self.name))
            if self.can_eat():
                self.eat()
            else:
                self.think()


def main():
    forks = [Fork() for i in range(5)]
    philosophers = [Philosopher(forks[i], forks[(i+1) % 5], str(i)) for i in range(5)]

    for philosopher in philosophers:
        philosopher.start()


if __name__ == '__main__':
    main()
