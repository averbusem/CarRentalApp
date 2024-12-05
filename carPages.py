from tkinter import *

from config import FONT
from basePage import BasePage


class PreCarsPage(BasePage):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        from mainPage import MainPage
        self.set_previous_page(MainPage)

        self.all_cars_btn = Button(self, text="Просмотр всех машин", font=FONT, command=self.listOfCars)
        self.free_cars_btn = Button(self, text="Просмотр свободных машин", font=FONT, command=self.checkFreeCars)
        self.find_car_btn = Button(self, text="Найти авто", font=FONT, command=self.findCar)
        self.add_car_btn = Button(self, text="Добавить авто", font=FONT, command=self.addCar)
        self.delete_car_btn = Button(self, text="Удалить машину из автопарка", font=FONT, command=self.deleteCar)
        self.back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)

        self.name_txt = Label(text=f"Автопарк", font=("Arial", 25))
        self.name_txt.pack(pady=40)

        elements = [self.all_cars_btn, self.free_cars_btn, self.find_car_btn, self.add_car_btn, self.delete_car_btn,
                    self.back_btn]

        self.page_elements += elements
        self.page_elements.append(self.name_txt)

        [x.pack(pady=20) for x in elements]

    def listOfCars(self, *args, **kwargs):
        self.clear_p()
        all_cars_page = AllCarsPage(self.master)
        all_cars_page.set_previous_page(PreCarsPage)
        all_cars_page.pack(expand=True, anchor="center")

    def checkFreeCars(self, *args, **kwargs):
        self.clear_p()
        free_cars_page = FreeCarsPage(self.master)
        free_cars_page.set_previous_page(PreCarsPage)
        free_cars_page.pack(expand=True, anchor="center")

    def findCar(self, *args, **kwargs):
        self.clear_p()
        find_car_page = FindCarPage(self.master)
        find_car_page.set_previous_page(PreCarsPage)
        find_car_page.pack(expand=True, anchor="center")

    def addCar(self, *args, **kwargs):
        self.clear_p()
        add_car_page = AddCarPage(self.master)
        add_car_page.set_previous_page(PreCarsPage)
        add_car_page.pack(expand=True, anchor="center")

    def deleteCar(self, *args, **kwargs):
        self.clear_p()
        delete_car_page = DeleteCarPage(self.master)
        delete_car_page.set_previous_page(PreCarsPage)
        delete_car_page.pack(expand=True, anchor="center")


class AllCarsPage(BasePage):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        page_name_txt = Label(self, text="Просмотр всех авто", font=("Arial", 25))
        page_name_txt.pack(pady=30)

        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)
        back_btn.pack()


class FreeCarsPage(BasePage):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        page_name_txt = Label(self, text="Просмотр свободных авто", font=("Arial", 25))
        page_name_txt.pack(pady=30)

        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)
        back_btn.pack()


class FindCarPage(BasePage):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        page_name_txt = Label(self, text="Найти авто", font=("Arial", 25))
        page_name_txt.pack(pady=30)

        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)
        back_btn.pack()


class AddCarPage(BasePage):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        page_name_txt = Label(self, text="Добавить авто", font=("Arial", 25))
        page_name_txt.pack(pady=30)

        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)
        back_btn.pack()


class DeleteCarPage(BasePage):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        page_name_txt = Label(self, text="Удалить авто", font=("Arial", 25))
        page_name_txt.pack(pady=30)

        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)
        back_btn.pack()


