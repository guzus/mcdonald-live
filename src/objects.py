import random


class Cashier:
    def __init__(self) -> None:
        self.customers = []

    def process(self, passed_time):
        if len(self.customers) == 0:
            return
        customer = self.customers[0]
        customer.paying_time -= passed_time
        if customer.paying_time <= 0:
            self.customers = self.customers[1:]

    def __repr__(self) -> str:
        return f"{self.customers}"


class Customer:
    def __init__(self, paying_time_mu, paying_time_sigma, cashiers) -> None:
        self.paying_time = round(
            random.normalvariate(paying_time_mu, paying_time_sigma), 1
        )
        self.cashier = min(cashiers, key=lambda x: (len(x.customers), random.random()))
        self.cashier.customers.append(self)
        self.waiting_time = 0

    def relocate_cashier(self, cashiers):
        current_cashier = self.cashier
        other_cashiers = filter(lambda x: x != current_cashier, cashiers)
        self.cashier = min(
            other_cashiers, key=lambda x: (len(x.customers), random.random())
        )
        self.cashier.customers.append(self)

    def __repr__(self) -> str:
        return f"{self.cashier} | {self.paying_time}"
