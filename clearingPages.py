import tkinter.messagebox
from tkinter import *

from config import FONT
from basePage import BasePage


class PreClearingPage(BasePage):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        from mainPage import MainPage
        self.set_previous_page(MainPage)

        self.total_clearing_btn = Button(self, text="Очистка всей базы данных", font=FONT, command=self.totalClearing)
        self.cars_clearing_btn = Button(self, text="Очистка автопарка", font=FONT, command=self.carsClearing)
        self.clients_clearing_btn = Button(self, text="Очистка клиентской базы", font=FONT, command=self.clientsClearing)
        self.orders_clearing_btn = Button(self, text="Очистка базы заказов", font=FONT, command=self.ordersClearing)
        self.back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)

        self.name_txt = Label(text=f"Очистка баз данных", font=("Arial", 25))
        self.name_txt.pack(pady=40)

        elements = [self.total_clearing_btn, self.cars_clearing_btn, self.clients_clearing_btn, self.orders_clearing_btn,
                    self.back_btn]

        self.page_elements += elements
        self.page_elements.append(self.name_txt)

        [x.pack(pady=20) for x in elements]

    def totalClearing(self, *args, **kwargs):
        if tkinter.messagebox.askyesno(title="Очистка всех баз данных",
                                       message="Вы собираетесь очистить все базы данных\n\n"
                                               "Вы уверены?"):
            #реализовать логику удаления БД
            pass

    def carsClearing(self, *args, **kwargs):
        if tkinter.messagebox.askyesno(title="Очистка автопарка",
                                       message="Вы собираетесь очистить данные автопарка\n\n"
                                               "Вы уверены?"):
            #реализовать логику удаления БД
            pass

    def clientsClearing(self, *args, **kwargs):
        if tkinter.messagebox.askyesno(title="Очистка клиентской базы",
                                       message="Вы собираетесь очистить данные о всех клиентах\n\n"
                                               "Вы уверены?"):
            #реализовать логику удаления БД
            pass

    def ordersClearing(self, *args, **kwargs):
        if tkinter.messagebox.askyesno(title="Очистка заказов",
                                       message="Вы собираетесь очистить данные о всех заказах (кроме действующих)\n\n"
                                               "Вы уверены?"):
            #реализовать логику удаления БД
            pass