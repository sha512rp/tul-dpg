"""Python threading."""

from threading import Thread, Condition
import time
import random


class InsufficientBalanceException(Exception):
    pass


class Account:
    def __init__(self):
        self.condition = Condition()
        self.balance = 0

    def make_payment(self, amount):
        with self.condition:
            while not self.can_pay(amount):
                self.condition.wait()
            self.balance -= amount
            self.condition.notify()

    def receive_payment(self, amount):
        with self.condition:
            self.condition.wait_for(self.can_receive)
            self.balance += amount
            self.condition.notify()

    def can_pay(self, amount):
        return self.balance > amount

    def can_receive(self):
        return True


class MakePaymentThread(Thread):

    PAYMENT_AMOUNT = 5

    def __init__(self, account):
        self.account = account
        super(MakePaymentThread, self).__init__()

    def run(self):
        amount = MakePaymentThread.PAYMENT_AMOUNT
        for i in range(100):
            self.account.make_payment(amount)
            print("Balance decreased by: {:d}\nBalance: {:d}".format(amount, self.account.balance))
            # time.sleep(random.random())


class ReceivePaymentThread(Thread):

    PAYMENT_AMOUNT = 2

    def __init__(self, account):
        self.account = account
        super(ReceivePaymentThread, self).__init__()

    def run(self):
        amount = ReceivePaymentThread.PAYMENT_AMOUNT
        for i in range(300):
            self.account.receive_payment(amount)
            print("Balance increased by: {:d}\nBalance: {:d}".format(amount, self.account.balance))
            # time.sleep(random.random())


def main():
    account = Account()
    account.balance = 1000
    make_payment_thread = MakePaymentThread(account)
    receive_payment_thread = ReceivePaymentThread(account)

    receive_payment_thread.start()
    make_payment_thread.start()

    make_payment_thread.join()
    receive_payment_thread.join()

    print("End of main thread")


if __name__ == '__main__':
    main()
