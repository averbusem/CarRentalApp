from tkinter import *
from tkinter.messagebox import showinfo
import tkinter.messagebox

from config import USER, PASS


class LoginWindow(Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        elements = []
        login_text = Label(self, text="Ваш логин")
        pass_text = Label(self, text="Ваш пароль")
        self.login = Entry(self)
        self.password = Entry(self, show='*')

        self.accept_button = Button(self, text="Войти", command=self.signIn)

        elements += login_text, self.login, pass_text, self.password, self.accept_button


        self.login.bind("<Return>", self.signIn)
        self.password.bind("<Return>", self.signIn)

        [x.pack() for x in elements]


    def signIn(self, *args, **kwargs):
        if tkinter.messagebox.askyesno(title="Уверены?", message="Уверены в корректности данных?"):
            if self.login.get() == USER and self.password.get() == PASS:
                tkinter.messagebox.showinfo(title="Отлично", message="Вы успешно вошли в свой профиль!")
                self.forget()
            else:
                tkinter.messagebox.showerror(title="Ошибка", message="Проверьте корректность введённых данных!")