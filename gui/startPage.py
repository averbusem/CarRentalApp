from tkinter import *
from tkinter.messagebox import showinfo
import tkinter.messagebox

from gui.mainPage import MainPage
from gui.config import USER, PASS, FONT


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
            if self.login.get() == USER and self.password.get() == PASS:
                tkinter.messagebox.showinfo(title="Отлично", message="Вы успешно вошли в профиль!")
                self.forget()
                main_page = MainPage(self.master)
                main_page.pack(expand=True)
            else:
                tkinter.messagebox.showerror(title="Ошибка", message="Проверьте корректность введённых данных!")