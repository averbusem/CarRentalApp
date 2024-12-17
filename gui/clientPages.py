from tkinter import *

from db import db
from gui.basePage import BasePage
from gui.config import FONT
import logging


class PreClientsPage(BasePage):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        from gui.mainPage import MainPage
        self.set_previous_page(MainPage)

        self.all_clients_btn = Button(self, text="Просмотр всех клиентов", font=FONT, command=self.listOfClients)
        self.find_client_btn = Button(self, text="Найти клиента", font=FONT, command=self.findClient)
        self.add_client_btn = Button(self, text="Добавить клиента", font=FONT, command=self.addClient)
        self.delete_client_btn = Button(self, text="Удалить клиента", font=FONT, command=self.deleteClient)
        self.back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)

        self.name_txt = Label(text=f"Клиенты", font=("Arial", 25))
        self.name_txt.pack(pady=40)


        elements = [self.all_clients_btn, self.find_client_btn, self.add_client_btn, self.delete_client_btn,
                    self.back_btn]

        self.page_elements += elements
        self.page_elements.append(self.name_txt)

        [x.pack(pady=20) for x in elements]

    def listOfClients(self, *args, **kwargs):
        self.clear_p()
        clients_page = ClientsListPage(self.master)
        clients_page.set_previous_page(PreClientsPage)
        clients_page.pack(expand=True, anchor="center")

    def findClient(self, *args, **kwargs):
        self.clear_p()
        find_client_page = FindClientPage(self.master)
        find_client_page.set_previous_page(PreClientsPage)
        find_client_page.pack(expand=True, anchor="center")

    def addClient(self, *args, **kwargs):
        self.clear_p()
        add_client_page = AddClientPage(self.master)
        add_client_page.set_previous_page(PreClientsPage)
        add_client_page.pack(expand=True, anchor="center")

    def deleteClient(self, *args, **kwargs):
        self.clear_p()
        delete_client_page = DeleteClientPage(self.master)
        delete_client_page.set_previous_page(PreClientsPage)
        delete_client_page.pack(expand=True, anchor="center")


class ClientsListPage(BasePage):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        page_name_txt = Label(self, text="Список клиентов", font=("Arial", 25))
        page_name_txt.pack(pady=30)

        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)
        back_btn.pack()


class FindClientPage(BasePage):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        page_name_txt = Label(self, text="Найти информацию о клиенте", font=("Arial", 25))
        page_name_txt.pack(pady=120)

        enter_info = Label(self, text="Введите паспорт или почту", font=FONT)

        info_field = Entry(self, font=FONT)

        elements = [enter_info, info_field]

        self.page_elements += elements

        [x.pack(pady=10) for x in elements]

        find_btn = Button(self, text="Найти", font=FONT, command=self.findClient)
        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)

        find_btn.pack(pady=15)
        back_btn.pack(pady=15)

    # логика перехода на страницу с инфой о клиенте
    def findClient(self, *args, **kwargs):
        pass


class AddClientPage(BasePage):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.set_previous_page(PreClientsPage)

        page_name_txt = Label(text="Добавление клиента", font=("Arial", 25))
        page_name_txt.pack(pady=30)
        self.page_elements.append(page_name_txt)

        enter_passport = Label(self, text="Введите паспорт клиента", font=FONT)
        enter_name = Label(self, text="Введите имя клиента", font=FONT)
        enter_middle_name = Label(self, text="Введите фамилию клиента", font=FONT)
        enter_last_name = Label(self, text="Введите отчество клиента", font=FONT)
        enter_email = Label(self, text="Введите почту клиента", font=FONT)
        enter_number = Label(self, text="Введите номер телефона клиента", font=FONT)

        self.passport_field = Entry(self, font=FONT)
        self.name_field = Entry(self, font=FONT)
        self.middle_name_field = Entry(self, font=FONT)
        self.last_name_field = Entry(self, font=FONT)
        self.email_field = Entry(self, font=FONT)
        self.number_field = Entry(self, font=FONT)


        elements = [enter_passport, self.passport_field, enter_name, self.name_field, enter_middle_name,
                    self.middle_name_field, enter_last_name, self.last_name_field, enter_email, self.email_field,
                    enter_number, self.number_field]

        self.page_elements += elements

        [x.pack(pady=4) for x in elements]

        client_info = [self.passport_field.get(), self.name_field.get(), self.middle_name_field.get(),
                       self.last_name_field.get(), self.email_field.get(), self.number_field.get()]
        add_client_btn = Button(self, text="Добавить клиента", font=FONT, command=lambda: self.addClient(client_info))



        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)

        add_client_btn.pack(pady=10)
        back_btn.pack(pady=10)

    # функция добавления клиента
    def addClient(self, client_info: list):
        pass
        """
        db.add_customer(client_info[0], client_info[1], client_info[2], client_info[3], client_info[4],
                        client_info[5])
        logging.info(f"Добавлен клиент: {client_info[0]} | {client_info[1]} | {client_info[2]} | "
                     f"{client_info[3]} | {client_info[4]} | {client_info[5]}")
        """

class DeleteClientPage(BasePage):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.set_previous_page(PreClientsPage)

        page_name_txt = Label(text="Удаление клиента", font=("Arial", 25))
        page_name_txt.pack(pady=30)
        self.page_elements.append(page_name_txt)

        enter_email = Label(self, text="Введите паспорт или почту клиента", font=FONT)
        self.email_field = Entry(self, font=FONT)

        elements = [enter_email, self.email_field]

        self.page_elements += elements

        [x.pack(pady=15) for x in elements]

        delete_client_btn = Button(self, text="Удалить клиента", font=FONT, command=self.deleteClient)
        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)

        delete_client_btn.pack(pady=10)
        back_btn.pack(pady=10)

    # функция удаления клиента
    def deleteClient(self):
        pass
