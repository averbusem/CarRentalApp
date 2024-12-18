from tkinter import *
import tkinter.messagebox
from db.database import Database
from gui.mainPage import MainPage

class StartPage(Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.elements = []
        self.greet_msg = Label(self, text="CarRentalApp", font=("Arial", 25))
        self.login_text = Label(self, text="Ваш логин", font=("Arial", 14))
        self.pass_text = Label(self, text="Ваш пароль", font=("Arial", 14))
        self.login = Entry(self, font=("Arial", 14))
        self.password = Entry(self, show='*', font=("Arial", 14))

        self.accept_button = Button(self, text="Войти", command=self.signIn, font=("Arial", 14))

        self.elements += [self.login_text, self.login, self.pass_text, self.password, self.accept_button]

        self.login.bind("<Return>", self.signIn)
        self.password.bind("<Return>", self.signIn)

        self.greet_msg.pack(pady=50)
        [x.pack(pady=10) for x in self.elements]

    def signIn(self, *args, **kwargs):
        if tkinter.messagebox.askyesno(title="Уверены?", message="Уверены в корректности данных?"):
            username = self.login.get()
            password = self.password.get()
            try:
                # Попробуем подключиться с указанными данными
                db = Database(user=username, password=password)
                tkinter.messagebox.showinfo(title="Успех", message="Вы успешно вошли в систему!")

                # Переход на следующую страницу, передаем объект базы данных
                self.forget()
                main_page = MainPage(self.master, db)
                main_page.pack(expand=True)

            except Exception as e:
                tkinter.messagebox.showerror(title="Ошибка", message="Неверные данные для входа!")
