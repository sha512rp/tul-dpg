"""Python threading."""

from threading import Thread


class MyThread(Thread):
    def __init__(self, name):
        super(MyThread, self).__init__()
        self.name = name

    def run(self):
        for i in range(10):
            print(self.name)


def main():
    t1 = MyThread("thread1")
    t2 = MyThread("thread2")

    t1.start()
    t2.start()


if __name__ == '__main__':
    main()
