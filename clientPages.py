from tkinter import *

from config import FONT
from basePage import BasePage

class PreClientsPage(BasePage):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.all_clients_btn = Button(self, text="Просмотр всех клиентов", font=FONT, command=self.listOfClients)
        self.find_client_btn = Button(self, text="Найти клиента", font=FONT, command=self.findClient)
        self.add_client_btn = Button(self, text="Добавить клиента", font=FONT, command=self.addClient)
        self.delete_client_btn = Button(self, text="Удалить клиента", font=FONT, command=self.deleteClient)
        self.back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)

        self.name_txt = Label(text=f"Клиенты", font=("Arial", 25))
        self.name_txt.pack()


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
        from mainPage import JustTestPage
        check_p = JustTestPage(self.master)
        check_p.pack()

    def addClient(self, *args, **kwargs):
        self.clear_p()
        from mainPage import JustTestPage
        check_p = JustTestPage(self.master)
        check_p.pack()

    def deleteClient(self, *args, **kwargs):
        self.clear_p()
        from mainPage import JustTestPage
        check_p = JustTestPage(self.master)
        check_p.pack()


class ClientsListPage(BasePage):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        greet_msg = Label(self, text="CarRentalApp", font=("Arial", 25))

        greet_msg.pack(pady=50)

        self.back_btn = Button(text="Назад", font=FONT, command=self.goBack())
