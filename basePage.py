from tkinter import *

class BasePage(Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.previous_page_class = None
        self.page_elements = []

    def set_previous_page(self, page_class):
        self.previous_page_class = page_class

    def goBack(self, *args, **kwargs):
        if self.previous_page_class:
            self.clear_p()
            previous_page = self.previous_page_class(self.master)
            previous_page.pack(expand=True, anchor='center')

    def clear_p(self, *args, **kwargs):
        self.forget()
        for child in self.page_elements:
            child.forget()