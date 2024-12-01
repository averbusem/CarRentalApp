from tkinter import *
from loginPage import LoginWindow

class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("CarRentalApp")
        self.window.geometry("1280x720")
        self.login = LoginWindow(self.window)
        self.login.pack(expand=True, anchor="center")

    def loop(self):
        self.window.mainloop()
