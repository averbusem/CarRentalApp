from tkinter import Button, Label, Entry
from gui.basePage import BasePage
from gui.config import FONT
import logging


class PreClientsPage(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.db = db  # Сохраняем db в экземпляре класса

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
        clients_page = ClientsListPage(self.master, self.db)  # Передаем db
        clients_page.set_previous_page(PreClientsPage)
        clients_page.pack(expand=True, anchor="center")

    def findClient(self, *args, **kwargs):
        self.clear_p()
        find_client_page = FindClientPage(self.master, self.db)  # Передаем db
        find_client_page.set_previous_page(PreClientsPage)
        find_client_page.pack(expand=True, anchor="center")

    def addClient(self, *args, **kwargs):
        self.clear_p()
        add_client_page = AddClientPage(self.master, self.db)  # Передаем db
        add_client_page.set_previous_page(PreClientsPage)
        add_client_page.pack(expand=True, anchor="center")

    def deleteClient(self, *args, **kwargs):
        self.clear_p()
        delete_client_page = DeleteClientPage(self.master, self.db)  # Передаем db
        delete_client_page.set_previous_page(PreClientsPage)
        delete_client_page.pack(expand=True, anchor="center")


class ClientsListPage(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.db = db  # Сохраняем db

        page_name_txt = Label(self, text="Список клиентов", font=("Arial", 25))
        page_name_txt.pack(pady=30)

        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)
        back_btn.pack()


class FindClientPage(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.db = db  # Сохраняем db

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

    def findClient(self, *args, **kwargs):
        pass


class AddClientPage(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.db = db  # Сохраняем db

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

        add_client_btn = Button(self, text="Добавить клиента", font=FONT, command=self.addClient)
        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)

        add_client_btn.pack(pady=10)
        back_btn.pack(pady=10)

    def addClient(self):
        client_info = [
            self.passport_field.get().strip(),
            self.name_field.get().strip(),
            self.middle_name_field.get().strip(),
            self.last_name_field.get().strip(),
            self.email_field.get().strip(),
            self.number_field.get().strip()
        ]

        if any(not field for field in client_info):
            print("Error: Все поля должны быть заполнены!")
            return

        try:
            self.db.add_customer(client_info[0], client_info[1], client_info[2], client_info[3], client_info[4], client_info[5])
            print("Клиент успешно добавлен!")
        except Exception as e:
            logging.error(f"Ошибка при добавлении клиента: {e}")
            print("Не удалось добавить клиента. Проверьте корректность данных.")


class DeleteClientPage(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.db = db  # Сохраняем db

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

    def deleteClient(self):
        pass
