from tkinter import *

from config import FONT
from basePage import BasePage

class PreClientsPage(BasePage):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        from mainPage import MainPage
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
        page_name_txt.pack(pady=30)

        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)
        back_btn.pack()


class AddClientPage(BasePage):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        page_name_txt = Label(self, text="Новый клиент", font=("Arial", 25))
        page_name_txt.pack(pady=30)

        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)
        back_btn.pack()


class DeleteClientPage(BasePage):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        page_name_txt = Label(self, text="Удалить клиента", font=("Arial", 25))
        page_name_txt.pack(pady=30)

        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)
        back_btn.pack()

