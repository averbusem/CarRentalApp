import tkinter.messagebox
from tkinter import *

from db.database import Database
from gui.mainPage import MainPage

from .config import (ADMIN_LOGIN, ADMIN_PASS, FONT, OWNER_LOGIN, OWNER_PASS,
                     TITLE_FONT)


class StartPage(Frame):
    def __init__(self, master, on_login_success, *args, **kwargs):
        """
        :param master: Родительский объект.
        :param on_login_success: Callback-функция для передачи объекта базы данных в App.
        """
        super().__init__(master, *args, **kwargs)
        self.on_login_success = on_login_success  # Callback для передачи объекта базы данных

        self.greet_msg = Label(self, text="CarRentalApp", font=TITLE_FONT)
        self.login_text = Label(self, text="Ваш логин", font=FONT)
        self.pass_text = Label(self, text="Ваш пароль", font=FONT)
        self.login = Entry(self, font=FONT)
        self.password = Entry(self, show='*', font=FONT)
        self.accept_button = Button(self, text="Войти", command=self.signIn, font=FONT)

        self.greet_msg.pack(pady=50)
        self.login_text.pack(pady=10)
        self.login.pack(pady=10)
        self.pass_text.pack(pady=10)
        self.password.pack(pady=10)
        self.accept_button.pack(pady=10)

        self.login.bind("<Return>", self.signIn)
        self.password.bind("<Return>", self.signIn)

    def signIn(self, *args, **kwargs):
        if tkinter.messagebox.askyesno(title="Уверены?", message="Уверены в корректности данных?"):
            username = self.login.get()
            password = self.password.get()

            if not ((username == ADMIN_LOGIN and password == ADMIN_PASS) or (username == OWNER_LOGIN and password == OWNER_PASS)):
                tkinter.messagebox.showerror(title="Ошибка", message="Неверные данные для входа!")
                return

            try:
                # Подключение к базе данных
                db = Database(user=username, password=password)
                tkinter.messagebox.showinfo(title="Успех", message="Вы успешно вошли в систему!")

                # Передача объекта базы данных в App через callback
                self.on_login_success(db)

                # Переход на следующую страницу
                self.pack_forget()  # Убираем текущий экран
                main_page = MainPage(self.master, db)
                main_page.pack(expand=True)

            except Exception as e:
                tkinter.messagebox.showerror(title="Ошибка", message=f"Ошибка подключения: {e}")
