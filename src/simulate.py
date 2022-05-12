import random
import time
import math
from draw import draw, draw_opening
from objects import Customer, Cashier


def spawn_customer(probability, paying_time_mu, paying_time_sigma, cashiers):
    if random.random() < probability:
        customer = Customer(paying_time_mu, paying_time_sigma, cashiers)
        return [customer]
    return []


def increase_cashier(cashiers):
    cashiers.append(Cashier())


def decrease_cashier(cashiers):
    if len(cashiers) > 1:
        # relocate customer
        removing_cashier = cashiers[-1]
        for customer in removing_cashier.customers:
            customer.relocate_cashier(cashiers)
        del cashiers[-1]


def rebalance_cashiers(do_not_distrub_cnt, event_period):
    message = """
    (i) increase_cashier
    (d) decrease_cashier
    (s) do not disturb for 60 sec
    > """
    if do_not_distrub_cnt > 0:
        do_not_distrub_cnt -= 1
    else:
        char_input = input(message)
        if char_input == "i":
            increase_cashier(cashiers)
        elif char_input == "d":
            decrease_cashier(cashiers)
        elif char_input == "s":
            do_not_distrub_cnt += 60 // event_period
        else:
            pass


if __name__ == "__main__":
    # game setting data class
    cashier_cnt_at_start = 4
    interval = 0.1
    cashiers = [Cashier() for _ in range(cashier_cnt_at_start)]
    spawn_probability_per_sec_mu = 2.5
    # customer intensity
    spawn_probability_per_sec_sigma = 1.0
    customer_flow_period = 10  # sec
    customers = []
    paying_time_mu = 1.5
    paying_time_sigma = 0.5
    total_waiting_time = 0
    total_spawned_customers = 0
    waiting_time_average = 0
    elapsed_time = 0
    do_not_distrub_cnt = 0
    event_period = 5

    draw_opening()
    while True:
        # event
        if elapsed_time % event_period > event_period - interval:
            rebalance_cashiers(do_not_distrub_cnt, event_period)

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
            (
                spawn_probability_per_sec_mu
                + spawn_probability_per_sec_sigma
                * math.cos(2 * math.pi / customer_flow_period * elapsed_time)
            )
            * interval,
            paying_time_mu,
            paying_time_sigma,
            cashiers,
        )
        customers += spawned_customers
        total_spawned_customers += len(spawned_customers)
        elapsed_time += interval

        draw(cashiers, elapsed_time, waiting_time_average)

        time.sleep(interval)
