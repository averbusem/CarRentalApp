import logging
import tkinter.messagebox
from tkinter import Button, Entry, Label
import re

from gui.basePage import BasePage
from gui.config import FONT, TITLE_FONT


class PreClientsPage(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, db, *args, **kwargs)
        from gui.mainPage import MainPage
        self.set_previous_page(MainPage)

        self.all_clients_btn = Button(self, text="Просмотр всех клиентов", font=FONT, command=self.listOfClients)
        self.find_client_btn = Button(self, text="Найти клиента", font=FONT, command=self.findClient)
        self.add_client_btn = Button(self, text="Добавить клиента", font=FONT, command=self.addClient)
        self.delete_client_btn = Button(self, text="Удалить клиента", font=FONT, command=self.deleteClient)
        self.back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)

        self.name_txt = Label(text=f"Клиенты", font=TITLE_FONT)
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


from tkinter import Canvas, Frame, Scrollbar, Label
from gui.basePage import BasePage
from gui.config import FONT, TITLE_FONT

class ClientsListPage(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, db, *args, **kwargs)
        self.set_previous_page(PreClientsPage)

        self.title_label = Label(self, text="Список всех клиентов", font=TITLE_FONT)
        self.title_label.pack(pady=20)

        # Обертка для прокручиваемой области
        self.scroll_frame = Frame(self)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Canvas для прокрутки (занимает половину ширины приложения)
        self.canvas = Canvas(self.scroll_frame, width=self.master.winfo_screenwidth() // 2)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Scrollbar
        self.scrollbar = Scrollbar(self.scroll_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Внутренний Frame для размещения содержимого
        self.inner_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Загрузка данных клиентов
        self.load_clients()

        # Настройка прокрутки
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

        self.back_button = Button(self, text="Назад", font=FONT, command=self.goBack)
        self.back_button.pack(pady=20)

    def load_clients(self):
        clients = self.db.get_all_customers()
        if not clients:
            no_data_label = Label(self.inner_frame, text="Нет данных о клиентах.", font=FONT)
            no_data_label.pack(pady=10)
            return

        # Отображение клиентов в виде списка
        for i, client in enumerate(clients, start=1):
            client_info = (f"{i}. {client['passport_number']} - "
                           f"{client['middle_name']} {client['first_name']} {client['last_name']} - "
                           f"{client['email']} - {client['phone_number']}")
            client_label = Label(self.inner_frame, text=client_info, font=FONT, anchor="w", justify="left")
            client_label.pack(fill="x", padx=10, pady=5)

    def _on_mouse_wheel(self, event):
        """Обрабатывает прокрутку колесиком мыши."""
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")


class FindClientPage(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, db, *args, **kwargs)

        page_name_txt = Label(self, text="Найти информацию о клиенте", font=TITLE_FONT)
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
        """Ищет клиента по паспорту или почте."""
        client_info = self.page_elements[1].get().strip()  # Получаем введённое значение из Entry
        print(client_info)

        if not client_info:
            tkinter.messagebox.showwarning(title="Внимание!", message="Поле поиска не может быть пустым!")
            return

        # Проверка формата паспорта или почты
        is_passport = client_info.isdigit() and len(client_info) == 10
        is_email = re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", client_info)

        if not (is_passport or is_email):
            tkinter.messagebox.showwarning(
                title="Ошибка!",
                message="Введите корректный номер паспорта (10 цифр) или email в правильном формате."
            )
            return

        try:
            # Получение информации о клиенте из базы данных
            client = self.db.find_customer_by_passport_or_email(client_info)
            if not client:
                tkinter.messagebox.showinfo(
                    title="Результат поиска",
                    message="Клиент с указанными данными не найден."
                )
                return

            # Получаем первый элемент списка
            client = client[0]

            # Отображение информации о клиенте
            client_data = (
                f"Паспорт: {client['passport_number']}\n"
                f"ФИО: {client['middle_name']} {client['first_name']} {client['last_name']}\n"
                f"Email: {client['email']}\n"
                f"Телефон: {client['phone_number']}"
            )
            tkinter.messagebox.showinfo(
                title="Информация о клиенте",
                message=client_data
            )
        except Exception as e:
            logging.error(f"Ошибка при поиске клиента: {e}")
            tkinter.messagebox.showerror(
                title="Ошибка!",
                message="Произошла ошибка при поиске клиента. Проверьте корректность данных и повторите попытку."
            )


class AddClientPage(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, db, *args, **kwargs)

        self.set_previous_page(PreClientsPage)

        page_name_txt = Label(text="Добавление клиента", font=TITLE_FONT)
        page_name_txt.pack(pady=30)
        self.page_elements.append(page_name_txt)

        enter_passport = Label(self, text="Введите паспорт клиента (10 символов)", font=FONT)
        enter_name = Label(self, text="Введите имя клиента (пример: Иван)", font=FONT)
        enter_middle_name = Label(self, text="Введите фамилию клиента (пример: Иванов)", font=FONT)
        enter_last_name = Label(self, text="Введите отчество клиента (пример: Иванович)", font=FONT)
        enter_email = Label(self, text="Введите почту клиента (пример: example@mail.ru)", font=FONT)
        enter_number = Label(self, text="Введите номер телефона клиента (11 символов)", font=FONT)

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

        if not (len(client_info[0]) == 10 and client_info[0].isdigit() and #корректность паспорта
                client_info[1].isalpha() and client_info[1].istitle() and #корректность ФИО
                client_info[2].isalpha() and client_info[2].istitle() and
                client_info[3].isalpha() and client_info[3].istitle() and
                re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", client_info[4]) and #корректность почты
                re.match(r"^\+?[0-9]{11}$", client_info[5]) and #корректность телефона
                all(field for field in client_info)): #если заполненны все поля
            tkinter.messagebox.showwarning(title="Внимательнее", message="Все поля должны быть заполнены правильно!")
            return

        try:
            self.db.add_customer(client_info[0], client_info[1], client_info[2], client_info[3], client_info[4], client_info[5])
            tkinter.messagebox.showinfo(title="Успешно!", message="Клиент успешно добавлен!")
        except Exception as e:
            logging.error(f"Ошибка при добавлении клиента: {e}")
            tkinter.messagebox.showerror(title="Ошибка!", message="Не удалось добавить клиента. Проверьте корректность данных.")


class DeleteClientPage(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, db, *args, **kwargs)

        self.set_previous_page(PreClientsPage)

        page_name_txt = Label(text="Удаление клиента", font=TITLE_FONT)
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
        client_info = self.email_field.get().strip()

        if not client_info:
            tkinter.messagebox.showwarning(title="Внимательнее!", message="Должны быть заполнены все поля!")
            return

        try:
            self.db.delete_customer_by_passport_or_email(client_info)
            tkinter.messagebox.showinfo(title="Успешно!", message="Клиент успешно удалён!")
        except Exception as e:
            logging.error(f"Ошибка при добавлении клиента: {e}")
            tkinter.messagebox.showerror(title="Ошибка!",
                                         message="Не удалось добавить клиента. Проверьте корректность данных.")
