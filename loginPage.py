from tkinter import *
from tkinter.messagebox import showinfo
import tkinter.messagebox

from config import USER, PASS, FONT

class StartPage(Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        greet_msg = Label(self, text="CarRentalApp", font=("Arial", 25))

        self.login_btn = Button(self, text="Войти", command=self.enableLogin, font=FONT)
        self.register_btn = Button(self, text="Зарегистрироваться", command=self.enableRegister, font=FONT)

        greet_msg.pack(pady=15)
        self.login_btn.pack(pady=15)
        self.register_btn.pack(pady=15)

    def enableLogin(self, *args, **kwargs):
        self.forget()
        LoginWindow(self.master).pack()


    def enableRegister(self, *args, **kwargs):
        self.forget()
        RegisterWindow(self.master).pack()


class LoginWindow(Frame):
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
                tkinter.messagebox.showinfo(title="Отлично", message="Вы успешно вошли в свой профиль!")
                self.forget()
            else:
                tkinter.messagebox.showerror(title="Ошибка", message="Проверьте корректность введённых данных!")


class RegisterWindow(Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        elements = []
        greet_msg = Label(self, text="CarRentalApp", font=("Arial", 25))
        login_text = Label(self, text="Придумайте Ваш логин", font=FONT)
        pass_text = Label(self, text="Придумайте Ваш пароль", font=FONT)
        repeat_pass_text = Label(self, text="Повторите Ваш пароль", font=FONT)

        self.login = Entry(self, font=FONT)
        self.password = Entry(self, show='*', font=FONT)
        self.repeat_password = Entry(self, show='*', font=FONT)

        self.accept_button = Button(self, text="Войти", command=self.regCommand, font=FONT)

        elements += (login_text, self.login, pass_text, self.password, repeat_pass_text, self.repeat_password,
                     self.accept_button)


        self.login.bind("<Return>", self.regCommand)
        self.password.bind("<Return>", self.regCommand)
        self.repeat_password.bind("<Return>", self.regCommand)

        greet_msg.pack(pady=50)
        [x.pack(pady=10) for x in elements]


    def regCommand(self, *args, **kwargs):
        if tkinter.messagebox.askyesno(title="Уверены?", message="Уверены в корректности данных?"):
            #Нужна проверка что юзера еще нет в системе
            if self.password.get() == self.repeat_password.get():
                tkinter.messagebox.showinfo(title="Отлично", message="Вы успешно зарегистрировались!")
                self.forget()
            else:
                tkinter.messagebox.showerror(title="Ошибка", message="Проверьте корректность введённых данных!")