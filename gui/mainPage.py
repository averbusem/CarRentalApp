import logging
import tkinter.messagebox
from tkinter import *

from gui.basePage import BasePage
from gui.carPages import PreCarsPage
from gui.clearingPages import PreClearingPage
from gui.clientPages import PreClientsPage
from gui.config import FONT, TITLE_FONT
from gui.orderPages import PreOrdersPage


class MainPage(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        # Передаем объект базы данных (db) и передаем его в родительский класс
        super().__init__(master, db, *args, **kwargs)

        self.clearing_btn = Button(self, text="Чистка базы данных", font=FONT, command=self.goToClearing, width=23)
        self.orders_btn = Button(self, text="Заказы", font=FONT, command=self.goToOrders, width=23)
        self.cars_btn = Button(self, text="Автопарк", font=FONT, command=self.goToCars, width=23)
        self.clients_btn = Button(self, text="Клиенты", font=FONT, command=self.goToClients, width=23)
        self.test_data_btn = Button(self, text="Внести тестовые данные", font=FONT, command=self.insertTestData, width=23)
        self.earnings_txt = Label(text=f"Выручка:\n\n\n${0}", font=TITLE_FONT)

        self.earnings_txt.pack(side=LEFT, padx=260)

        elements = [self.clearing_btn, self.orders_btn, self.cars_btn, self.clients_btn, self.test_data_btn]

        self.page_elements += elements
        self.page_elements.append(self.earnings_txt)

        [x.pack(anchor='e', pady=20) for x in elements]


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

    def insertTestData(self):
        if tkinter.messagebox.askyesno(title="Добавление тестовых данных",
                                       message="Вы собираетесь внести тестовые данные\n\n"
                                               "Вы уверены?"):
            try:
                self.db.insert_test_data()  # Вызов функции очистки всех таблиц
                tkinter.messagebox.showinfo(title="Успешно!", message="Тестовые данные добавлены!")
                print("Test data inserted successfully")
            except Exception as e:
                logging.error(f"Ошибка при добавлении тестовых данных: {e}")
                print("Failed to insert test data")
                tkinter.messagebox.showerror(title="Ошибка!", message=f"Не удалось добавить тестовые данные: {e}")

class JustTestPage(BasePage):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        greet_msg = Label(self, text="CarRentalApp", font=TITLE_FONT)

        greet_msg.pack(pady=50)
