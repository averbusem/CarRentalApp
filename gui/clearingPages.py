import tkinter.messagebox
from tkinter import *

from gui.basePage import BasePage
from gui.config import FONT, TITLE_FONT


class PreClearingPage(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, db=db, *args, **kwargs)

        from gui.mainPage import MainPage
        self.set_previous_page(MainPage)

        self.total_clearing_btn = Button(self, text="Очистка всей базы данных", font=FONT, command=self.totalClearing, width=25)
        self.cars_clearing_btn = Button(self, text="Очистка автопарка", font=FONT, command=self.carsClearing, width=25)
        self.clients_clearing_btn = Button(self, text="Очистка клиентской базы", font=FONT, command=self.clientsClearing, width=25)
        self.orders_clearing_btn = Button(self, text="Очистка базы заказов", font=FONT, command=self.ordersClearing, width=25)
        self.back_btn = Button(self, text="Назад", font=FONT, command=self.goBack, width=10)

        self.name_txt = Label(text=f"Очистка баз данных", font=TITLE_FONT)
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
            # Реализовать логику удаления всех баз данных
            pass

    def carsClearing(self, *args, **kwargs):
        if tkinter.messagebox.askyesno(title="Очистка автопарка",
                                       message="Вы собираетесь очистить данные автопарка\n\n"
                                               "Вы уверены?"):
            # Реализовать логику удаления данных автопарка
            pass

    def clientsClearing(self, *args, **kwargs):
        if tkinter.messagebox.askyesno(title="Очистка клиентской базы",
                                       message="Вы собираетесь очистить данные о всех клиентах\n\n"
                                               "Вы уверены?"):
            # Реализовать логику удаления данных о клиентах
            pass

    def ordersClearing(self, *args, **kwargs):
        if tkinter.messagebox.askyesno(title="Очистка заказов",
                                       message="Вы собираетесь очистить данные о всех заказах (кроме действующих)\n\n"
                                               "Вы уверены?"):
            # Реализовать логику удаления данных о заказах
            pass
