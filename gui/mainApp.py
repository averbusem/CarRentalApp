from tkinter import *
from tkinter import messagebox

from gui.startPage import StartPage


class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("CarRentalApp")
        self.window.geometry("1280x720")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.db_connection = None  # Переменная для хранения подключения к базе данных

        # Инициализация стартовой страницы
        self.start_page = StartPage(self.window, self.on_login_success)
        self.start_page.pack(expand=True)

    def on_login_success(self, db_connection):
        """
        Вызывается после успешного входа, передается объект подключения к БД.
        """
        self.db_connection = db_connection

    def close_database_connection(self):
        """
        Закрытие подключения к базе данных.
        """
        if self.db_connection:
            self.db_connection.close_connection()

    def on_close(self):
        """
        Закрытие приложения.
        """
        if messagebox.askyesno("Выход", "Вы уверены, что хотите выйти?"):
            self.close_database_connection()
            self.window.destroy()

    def loop(self):
        self.window.mainloop()
