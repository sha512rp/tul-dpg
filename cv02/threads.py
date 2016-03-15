"""Python threading."""

from threading import Thread, Condition
import time


class StorageFullException(Exception):
    pass


class StorageEmptyException(Exception):
    pass


class Storage:
    def __init__(self, capacity=3):
        self.condition = Condition()
        self.data = []
        self.capacity = capacity

    def create_item(self, item):
        if not self.is_not_full():
            raise StorageFullException
        self.data.append(item)

    def take_item(self):
        if not self.has_item():
            raise StorageEmptyException
        return self.data.pop()

    def has_item(self):
        return not self.data

    def is_not_full(self):
        return len(self.data) < self.capacity


class ProducerThread(Thread):
    def __init__(self, storage):
        self.storage = storage
        super(ProducerThread, self).__init__()

    def run(self):
        for i in range(10):
            with self.storage.condition as cond:
                self.storage.condition.wait_for(self.storage.is_not_full)
                self.storage.create_item(i)
                print("Produced: %d" % i)
                self.storage.condition.notify_all()


class ConsumerThread(Thread):
    def __init__(self, storage):
        self.storage = storage
        super(ConsumerThread, self).__init__()

    def run(self):
        for i in range(10):
            with self.storage.condition as cond:
                self.storage.condition.wait_for(self.storage.has_item)
                item = self.storage.take_item()
                print("Consumed: %d" % item)
                self.storage.condition.notify_all()


class MyThread(Thread):
    def __init__(self, name):
        super(MyThread, self).__init__()
        self.name = name

    def run(self):
        for i in range(10):
            time.sleep(0.1)
            print("Running thread: " + self.name)


class MyWaitingThread(Thread):
    def __init__(self, name, wait_time):
        super(MyWaitingThread, self).__init__()
        self.name = name
        self.wait_time = wait_time
        self.counter = 0

    def run(self):
        for i in range(10):
            self.counter += 1
            time.sleep(self.wait_time)
            # print("Thread %s: %d" % (self.name, self.counter))


def main_prod_cons():
    storage = Storage(capacity=3)
    producers = []
    consumers = []

    for i in range(1):
        producers.append(ProducerThread(storage).start())

    for i in range(1):
        consumers.append(ConsumerThread(storage).start())





def main_waiting():
    t1 = MyWaitingThread("thread1", 1.3)
    t2 = MyWaitingThread("thread2", 0.8)

    t1.start()
    t2.start()

    while True:
        if t1.counter > 4 or t2.counter > 4:
            print("Done!")
            break
        else:
            print(".")
        time.sleep(0.3)

    t1.join()
    t2.join()



def main():
    t1 = MyThread("thread1")
    t2 = MyThread("thread2")

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("End of main thread")


if __name__ == '__main__':
    main_prod_cons()
