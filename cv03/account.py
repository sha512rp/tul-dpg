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
        # with self.condition:
        if amount > self.balance:
            raise InsufficientBalanceException
        self.balance -= amount

    def receive_payment(self, amount):
        # with self.condition:
        self.balance += amount

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
            with self.account.condition:
                while not self.account.can_pay(amount):
                    self.account.condition.wait()
                self.account.make_payment(amount)
                print("Balance decreased by: {:d}\nBalance: {:d}".format(amount, self.account.balance))
                self.account.condition.notify_all()
            # time.sleep(random.random())


class ReceivePaymentThread(Thread):

    PAYMENT_AMOUNT = 2

    def __init__(self, account):
        self.account = account
        super(ReceivePaymentThread, self).__init__()

    def run(self):
        amount = ReceivePaymentThread.PAYMENT_AMOUNT
        for i in range(300):
            with self.account.condition:
                while not self.account.can_receive():
                    self.account.condition.wait()
                self.account.receive_payment(amount)
                print("Balance increased by: {:d}\nBalance: {:d}".format(amount, self.account.balance))
                self.account.condition.notify_all()
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
