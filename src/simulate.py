import random
import time
from draw import draw


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

    def __repr__(self) -> str:
        return f"{self.cashier} | {self.paying_time}"


def spawn_customer(probability, paying_time_mu, paying_time_sigma, cashiers):
    if random.random() < probability:
        customer = Customer(paying_time_mu, paying_time_sigma, cashiers)
        return [customer]
    return []


cashier_cnt = 4
interval = 0.01
cashiers = [Cashier() for _ in range(cashier_cnt)]
spawn_probability_per_sec = 2.5
customers = []
paying_time_mu = 1
paying_time_sigma = 0.5
total_waiting_time = 0
total_spawned_customers = 0
waiting_time_average = 0

while True:
    for cashier in cashiers:
        cashier.process(interval)
        for customer in cashier.customers:
            customer.waiting_time += interval
        total_waiting_time += len(cashier.customers) * interval
    waiting_time_average = (
        total_waiting_time / total_spawned_customers
        if total_spawned_customers > 0
        else 0
    )

    spawned_customers = spawn_customer(
        # TODO: poisson distribution
        spawn_probability_per_sec * interval,
        paying_time_mu,
        paying_time_sigma,
        cashiers,
    )
    customers += spawned_customers
    total_spawned_customers += len(spawned_customers)

    draw(cashiers, waiting_time_average)

    time.sleep(interval)
