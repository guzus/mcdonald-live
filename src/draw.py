import os


def draw(cashiers, waiting_time_average):
    cls()
    img = "McDonald\n"
    for cashier in cashiers:
        img += f"*" + "|" + "." * len(cashier.customers) + "\n"
    img += f"waiting_time_average : {round(waiting_time_average, 2)}"
    print(img)


def cls():
    os.system("cls" if os.name == "nt" else "clear")
