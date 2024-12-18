from tkinter import *

from gui.basePage import BasePage
from gui.carPages import PreCarsPage
from gui.clearingPages import PreClearingPage
from gui.clientPages import PreClientsPage
from gui.config import FONT, TITLE_FONT
from gui.orderPages import CloseOrderPage, NewOrderPage, PreOrdersPage


class MainPage(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        # Передаем объект базы данных (db) и передаем его в родительский класс
        super().__init__(master, db, *args, **kwargs)

        self.create_order_btn = Button(self, text="Создать заказ", font=FONT, command=self.goToNewOrder)
        self.close_order_btn = Button(self, text="Закрыть заказ", font=FONT, command=self.goToClosingOrder)
        self.clearing_btn = Button(self, text="Чистка базы данных", font=FONT, command=self.goToClearing)
        self.orders_btn = Button(self, text="Заказы", font=FONT, command=self.goToOrders)
        self.cars_btn = Button(self, text="Автопарк", font=FONT, command=self.goToCars)
        self.clients_btn = Button(self, text="Клиенты", font=FONT, command=self.goToClients)

        self.earnings_txt = Label(text=f"Выручка:\n\n\n${0}", font=TITLE_FONT)

        self.earnings_txt.pack(side=LEFT, padx=260)

        elements = [self.create_order_btn, self.close_order_btn, self.clearing_btn, self.orders_btn, self.cars_btn,
                    self.clients_btn]

        self.page_elements += elements
        self.page_elements.append(self.earnings_txt)

        [x.pack(anchor='e', pady=20) for x in elements]

    def goToNewOrder(self, *args, **kwargs):
        self.clear_p()
        new_order_p = NewOrderPage(self.master, self.db)  # Передаем db в NewOrderPage
        new_order_p.pack(expand=True, anchor='center')

    def goToClosingOrder(self, *args, **kwargs):
        self.clear_p()
        close_order_p = CloseOrderPage(self.master, self.db)  # Передаем db
        close_order_p.pack(expand=True, anchor='center')

    def goToClearing(self, *args, **kwargs):
        self.clear_p()
        clearing_p = PreClearingPage(self.master, self.db)  # Передаем db
        clearing_p.pack(expand=True, anchor='center')

    def goToOrders(self, *args, **kwargs):
        self.clear_p()
        orders_p = PreOrdersPage(self.master, self.db)  # Передаем db
        orders_p.pack(expand=True, anchor='center')

    def goToCars(self, *args, **kwargs):
        self.clear_p()
        car_p = PreCarsPage(self.master, self.db)  # Передаем db
        car_p.pack(expand=True, anchor='center')

    def goToClients(self, *args, **kwargs):
        self.clear_p()
        pcp = PreClientsPage(self.master, self.db)  # Передаем db
        pcp.pack(expand=True, anchor='center')


class JustTestPage(BasePage):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        greet_msg = Label(self, text="CarRentalApp", font=TITLE_FONT)

        greet_msg.pack(pady=50)
