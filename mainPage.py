from tkinter import *

from config import FONT


class MainPage(Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.page_elements = []

        self.create_order_btn = Button(self, text="Создать заказ", font=FONT, command=self.goToNewOrder)
        self.clearing_btn = Button(self, text="Чистка базы данных", font=FONT, command=self.goToClearing)
        self.orders_btn = Button(self, text="Заказы", font=FONT, command=self.goToOrders)
        self.cars_btn = Button(self, text="Автопарк", font=FONT, command=self.goToCars)
        self.clients_btn = Button(self, text="Клиенты", font=FONT, command=self.goToClients)

        self.earnings_txt = Label(text=f"Выручка:\n\n\n${0}", font=("Arial", 25))

        self.earnings_txt.pack(side=LEFT, padx=260)

        elements = [self.create_order_btn, self.clearing_btn, self.orders_btn, self.cars_btn, self.clients_btn]

        self.page_elements += elements
        self.page_elements.append(self.earnings_txt)

        [x.pack(anchor='e', pady=20) for x in elements]

    def clear_p(self, *args, **kwargs):
        self.forget()
        for el in self.page_elements:
            el.forget()

    def goToNewOrder(self, *args, **kwargs):
        self.clear_p()
        check_p = JustTestPage(self.master)
        check_p.pack()

    def goToClearing(self, *args, **kwargs):
        self.clear_p()
        check_p = JustTestPage(self.master)
        check_p.pack()

    def goToOrders(self, *args, **kwargs):
        self.clear_p()
        check_p = JustTestPage(self.master)
        check_p.pack()

    def goToCars(self, *args, **kwargs):
        self.clear_p()
        check_p = JustTestPage(self.master)
        check_p.pack()

    def goToClients(self, *args, **kwargs):
        self.clear_p()
        check_p = JustTestPage(self.master)
        check_p.pack()

class JustTestPage(Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        greet_msg = Label(self, text="CarRentalApp", font=("Arial", 25))

        greet_msg.pack(pady=50)
