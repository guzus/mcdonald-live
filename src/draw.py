import os
import time


def draw(cashiers, elapsed_time, waiting_time_average):
    cls()
    img = "McDonald Simulation\n"
    img += f"elapsed_time : {round(elapsed_time, 2)}s\n\n"
    for cashier in cashiers:
        img += f"*" + "|" + "." * len(cashier.customers) + "\n"
    img += f"\nwaiting_time_average : {round(waiting_time_average, 2)}s"
    print(img)

def draw_opening():
    cls()
    print('''
    --McDonald Simulation--
    loading..
    ''')
    time.sleep(0.5)

def cls():
    os.system("cls" if os.name == "nt" else "clear")
