import logging
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
        self.delete_client_info_btn = Button(self, text="Удалить данные клиента", font=FONT, command=self.deleteClientInfo, width=25)
        self.back_btn = Button(self, text="Назад", font=FONT, command=self.goBack, width=10)

        self.name_txt = Label(text=f"Очистка баз данных", font=TITLE_FONT)
        self.name_txt.pack(pady=40)

        elements = [self.total_clearing_btn, self.cars_clearing_btn, self.clients_clearing_btn, self.orders_clearing_btn,
                    self.delete_client_info_btn, self.back_btn]

        self.page_elements += elements
        self.page_elements.append(self.name_txt)

        [x.pack(pady=20) for x in elements]

    def totalClearing(self, *args, **kwargs):
        if tkinter.messagebox.askyesno(title="Очистка всех баз данных",
                                       message="Вы собираетесь очистить все базы данных\n\n"
                                               "Вы уверены?"):
            try:
                self.db.clear_all_tables()  # Вызов функции очистки всех таблиц
                tkinter.messagebox.showinfo(title="Успешно!", message="Все таблицы успешно очищены!")
            except Exception as e:
                logging.error(f"Ошибка при очистке базы данных: {e}")
                tkinter.messagebox.showerror(title="Ошибка!", message=f"Не удалось очистить все таблицы: {e}")

    def carsClearing(self, *args, **kwargs):
        if tkinter.messagebox.askyesno(title="Очистка автопарка",
                                       message="Вы собираетесь очистить данные автопарка\n\n"
                                               "Вы уверены?"):
            try:
                self.db.clear_cars_table()  # Вызов функции очистки таблицы Cars
                tkinter.messagebox.showinfo(title="Успешно!", message="Таблица автопарка успешно очищена!")
            except Exception as e:
                logging.error(f"Ошибка при очистке автопарка: {e}")
                tkinter.messagebox.showerror(title="Ошибка!", message=f"Не удалось очистить таблицу автопарка: {e}")

    def clientsClearing(self, *args, **kwargs):
        if tkinter.messagebox.askyesno(title="Очистка клиентской базы",
                                       message="Вы собираетесь очистить данные о всех клиентах\n\n"
                                               "Вы уверены?"):
            try:
                self.db.clear_customers_table()  # Вызов функции очистки таблицы Customers
                tkinter.messagebox.showinfo(title="Успешно!", message="Таблица клиентов успешно очищена!")
            except Exception as e:
                logging.error(f"Ошибка при очистке клиентов: {e}")
                tkinter.messagebox.showerror(title="Ошибка!", message=f"Не удалось очистить таблицу клиентов: {e}")

    def ordersClearing(self, *args, **kwargs):
        if tkinter.messagebox.askyesno(title="Очистка заказов",
                                       message="Вы собираетесь очистить данные о всех заказах (кроме действующих)\n\n"
                                               "Вы уверены?"):
            try:
                self.db.clear_bookings_table()  # Вызов функции очистки таблицы Bookings
                tkinter.messagebox.showinfo(title="Успешно!", message="Таблица заказов успешно очищена!")
            except Exception as e:
                logging.error(f"Ошибка при очистке заказов: {e}")
                tkinter.messagebox.showerror(title="Ошибка!", message=f"Не удалось очистить таблицу заказов: {e}")

    def deleteClientInfo(self, *args, **kwargs):
        self.clear_p()
        clearing_p = ClearingClientInfo(self.master, self.db)
        clearing_p.pack(expand=True, anchor="center")

class ClearingClientInfo(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, db, *args, **kwargs)
        self.set_previous_page(PreClearingPage)

        page_name_txt = Label(text="Удаление данных клиента", font=TITLE_FONT)
        page_name_txt.pack(pady=30)
        self.page_elements.append(page_name_txt)

        enter_passport = Label(self, text="Введите паспорт клиента (10 цифр)", font=FONT)
        self.name_field = Entry(self, font=FONT)

        elements = [enter_passport, self.name_field]

        self.page_elements += elements

        [x.pack(pady=15) for x in elements]

        create_order_btn = Button(self, text="Удалить данные клиента", font=FONT, command=self.deleteClientInfo)
        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)

        create_order_btn.pack(pady=10)
        back_btn.pack(pady=10)

    # функция удаления клиента
    def deleteClientInfo(self):
        client_passport = self.name_field.get().strip()

        if not (client_passport.isdigit() and len(client_passport) == 10 and # паспорт - число и длина равна 10
                client_passport):
            tkinter.messagebox.showwarning(title="Внимательнее", message="Все поля должны быть заполнены правильно!")
            return

        try:
            self.db.delete_customer_fully(client_passport)
            tkinter.messagebox.showinfo(title="Успешно!", message="Вся информация о клиенте была удалена!")
        except Exception as e:
            logging.error(f"Ошибка при удалении информации: {e}")
            tkinter.messagebox.showerror(title="Ошибка!", message="Не удалось удалить информацию. Проверьте корректность данных.")