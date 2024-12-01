from tkinter import *
from loginPage import LoginWindow, StartPage

class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("CarRentalApp")
        self.window.geometry("1280x720")
        self.start = StartPage(self.window)
        self.start.pack(expand=True, anchor="center")

    def loop(self):
        self.window.mainloop()
