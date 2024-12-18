import tkinter.messagebox
from tkinter import *
from tkinter.messagebox import showinfo
from db.database import Database
from gui.config import FONT
from gui.mainPage import MainPage


class StartPage(Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        elements = []
        greet_msg = Label(self, text="CarRentalApp", font=("Arial", 25))
        login_text = Label(self, text="Ваш логин", font=FONT)
        pass_text = Label(self, text="Ваш пароль", font=FONT)
        self.login = Entry(self, font=FONT)
        self.password = Entry(self, show='*', font=FONT)

        self.accept_button = Button(self, text="Войти", command=self.signIn, font=FONT)

        elements += login_text, self.login, pass_text, self.password, self.accept_button


        self.login.bind("<Return>", self.signIn)
        self.password.bind("<Return>", self.signIn)

        greet_msg.pack(pady=50)
        [x.pack(pady=10) for x in elements]

    def signIn(self, *args, **kwargs):
        if tkinter.messagebox.askyesno(title="Уверены?", message="Уверены в корректности данных?"):
            username = self.login.get()
            password = self.password.get()
            try:
                # Создаём объект базы данных
                db_instance = Database(user=username, password=password)
                tkinter.messagebox.showinfo(title="Успех", message="Вы успешно вошли в систему!")

                # Переходим на главную страницу, передавая объект базы данных
                self.forget()
                main_page = MainPage(self.master, db=db_instance)
                main_page.pack(expand=True)
            except Exception as e:
                tkinter.messagebox.showerror(title="Ошибка", message="Неверные данные для входа!")
