import logging
import tkinter
from tkinter import *
from tkinter import messagebox

from gui.basePage import BasePage
from gui.config import FONT, TITLE_FONT


class PreCarsPage(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, db, *args, **kwargs)

        from gui.mainPage import MainPage
        self.set_previous_page(MainPage)

        self.all_cars_btn = Button(self, text="Просмотр всех машин", font=FONT, command=self.listOfCars)
        self.free_cars_btn = Button(self, text="Просмотр свободных машин", font=FONT, command=self.checkFreeCars)
        self.find_car_btn = Button(self, text="Найти авто", font=FONT, command=self.findCar)
        self.add_car_btn = Button(self, text="Добавить авто", font=FONT, command=self.addCar)
        self.add_model_btn = Button(self, text="Добавить модель авто", font=FONT, command=self.addCarModel)
        self.delete_car_btn = Button(self, text="Удалить машину из автопарка", font=FONT, command=self.deleteCar)
        self.back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)

        self.name_txt = Label(text=f"Автопарк", font=TITLE_FONT)
        self.name_txt.pack(pady=40)

        elements = [self.all_cars_btn, self.free_cars_btn, self.find_car_btn, self.add_car_btn, self.delete_car_btn,
                    self.add_model_btn, self.back_btn]

        self.page_elements += elements
        self.page_elements.append(self.name_txt)

        [x.pack(pady=20) for x in elements]

    def listOfCars(self, *args, **kwargs):
        self.clear_p()
        all_cars_page = AllCarsPage(self.master, db=self.db)
        all_cars_page.set_previous_page(PreCarsPage)
        all_cars_page.pack(expand=True, anchor="center")

    def checkFreeCars(self, *args, **kwargs):
        self.clear_p()
        free_cars_page = FreeCarsPage(self.master, db=self.db)
        free_cars_page.set_previous_page(PreCarsPage)
        free_cars_page.pack(expand=True, anchor="center")

    def findCar(self, *args, **kwargs):
        self.clear_p()
        find_car_page = FindCarPage(self.master, db=self.db)
        find_car_page.set_previous_page(PreCarsPage)
        find_car_page.pack(expand=True, anchor="center")

    def addCar(self, *args, **kwargs):
        self.clear_p()
        add_car_page = AddCarPage(self.master, db=self.db)
        add_car_page.set_previous_page(PreCarsPage)
        add_car_page.pack(expand=True, anchor="center")

    def addCarModel(self, *args, **kwargs):
        self.clear_p()
        add_car_page = AddModelPage(self.master, db=self.db)
        add_car_page.set_previous_page(PreCarsPage)
        add_car_page.pack(expand=True, anchor="center")

    def deleteCar(self, *args, **kwargs):
        self.clear_p()
        delete_car_page = DeleteCarPage(self.master, db=self.db)
        delete_car_page.set_previous_page(PreCarsPage)
        delete_car_page.pack(expand=True, anchor="center")


class AllCarsPage(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, db, *args, **kwargs)
        page_name_txt = Label(self, text="Просмотр всех авто", font=TITLE_FONT)
        page_name_txt.pack(pady=30)

        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)
        back_btn.pack()


class FreeCarsPage(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, db, *args, **kwargs)
        page_name_txt = Label(self, text="Просмотр свободных авто", font=TITLE_FONT)
        page_name_txt.pack(pady=30)

        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)
        back_btn.pack()


class FindCarPage(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, db, *args, **kwargs)
        page_name_txt = Label(self, text="Найти авто", font=TITLE_FONT)
        page_name_txt.pack(pady=30)

        enter_brand = Label(self, text="Введите марку машин", font=FONT)
        enter_model = Label(self, text="Введите модель машин", font=FONT)

        brand_field = Entry(self, font=FONT)
        model_field = Entry(self, font=FONT)

        elements = [enter_brand, brand_field, enter_model, model_field]

        self.page_elements += elements

        [x.pack(pady=10) for x in elements]

        find_btn = Button(self, text="Найти", font=FONT, command=self.findCars)
        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)

        find_btn.pack(pady=15)
        back_btn.pack(pady=15)

    def findCars(self, *args, **kwargs):
        pass


class AddCarPage(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, db, *args, **kwargs)
        self.set_previous_page(PreCarsPage)

        page_name_txt = Label(text="Добавление авто", font=TITLE_FONT)
        page_name_txt.pack(pady=30)
        self.page_elements.append(page_name_txt)

        enter_vin = Label(self, text="Введите VIN авто", font=FONT)
        enter_number = Label(self, text="Введите гос номер авто", font=FONT)
        enter_brand = Label(self, text="Введите марку авто", font=FONT)
        enter_model = Label(self, text="Введите модель авто", font=FONT)
        enter_color = Label(self, text="Введите цвет машины", font=FONT)

        self.vin_field = Entry(self, font=FONT)
        self.number_field = Entry(self, font=FONT)
        self.brand_field = Entry(self, font=FONT)
        self.model_field = Entry(self, font=FONT)
        self.color_field = Entry(self, font=FONT)

        elements = [enter_vin, self.vin_field, enter_number, self.number_field, enter_brand,
                    self.brand_field, enter_model, self.model_field, enter_color, self.color_field]

        self.page_elements += elements

        [x.pack(pady=6) for x in elements]

        add_car_btn = Button(self, text="Добавить авто в автопарк", font=FONT, command=self.addCar)
        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)

        add_car_btn.pack(pady=10)
        back_btn.pack(pady=10)

    def addCar(self):
        car_info = [
            self.vin_field.get().strip(),
            self.number_field.get().strip(),
            self.brand_field.get().strip(),
            self.model_field.get().strip(),
            self.color_field.get().strip()
        ]

        if not all(field for field in car_info): #если заполненны все поля
            tkinter.messagebox.showwarning(title="Внимательнее", message="Все поля должны быть заполнены!")
            return

        try:
            self.db.add_car(car_info[0], car_info[1], car_info[2], car_info[3], car_info[4])
            tkinter.messagebox.showinfo(title="Успешно!", message="Машина успешно добавлена!")
        except Exception as e:
            logging.error(f"Ошибка при добавлении машины: {e}")
            tkinter.messagebox.showerror(title="Ошибка!", message="Не удалось добавить машину. Проверьте корректность данных.")


class AddModelPage(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, db, *args, **kwargs)
        self.set_previous_page(PreCarsPage)

        page_name_txt = Label(text="Добавление модели авто", font=TITLE_FONT)
        page_name_txt.pack(pady=30)
        self.page_elements.append(page_name_txt)

        enter_brand = Label(self, text="Введите марку", font=FONT)
        enter_model_name = Label(self, text="Введите название модели", font=FONT)
        enter_eng_volume = Label(self, text="Введите объём двигателя", font=FONT)
        enter_h_power = Label(self, text="Введите лошадинные силы авто", font=FONT)
        enter_transmission = Label(self, text="Введите КПП модели авто (мех, авто, робот)", font=FONT)
        enter_price = Label(self, text="Введите стоимость за день проката", font=FONT)

        self.brand_field = Entry(self, font=FONT)
        self.model_name_field = Entry(self, font=FONT)
        self.engine_volume = Entry(self, font=FONT)
        self.power_field = Entry(self, font=FONT)
        self.trans_field = Entry(self, font=FONT)
        self.price_field = Entry(self, font=FONT)

        elements = [enter_brand, self.brand_field, enter_model_name, self.model_name_field, enter_eng_volume,
                    self.engine_volume, enter_h_power, self.power_field, enter_transmission, self.trans_field,
                    enter_price, self.price_field]

        self.page_elements += elements

        [x.pack(pady=6) for x in elements]

        add_model_btn = Button(self, text="Добавить модель", font=FONT, command=self.addModel)
        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)

        add_model_btn.pack(pady=10)
        back_btn.pack(pady=10)

    def addModel(self):
        model_info = [
            self.brand_field.get().strip(),
            self.model_name_field.get().strip(),
            self.engine_volume.get().strip(),
            self.power_field.get().strip(),
            self.trans_field.get().strip(),
            self.price_field.get().strip()
        ]

        if not all(field for field in model_info): #если заполненны все поля
            tkinter.messagebox.showwarning(title="Внимательнее", message="Все поля должны быть заполнены!")
            return

        try:
            self.db.add_model(model_info[0], model_info[1], model_info[2], model_info[3], model_info[4], model_info[5])
            tkinter.messagebox.showinfo(title="Успешно!", message="Модель успешно добавлена!")
        except Exception as e:
            logging.error(f"Ошибка при добавлении модели: {e}")
            tkinter.messagebox.showerror(title="Ошибка!", message="Не удалось добавить модель. Проверьте корректность данных.")



class DeleteCarPage(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, db, *args, **kwargs)
        self.set_previous_page(PreCarsPage)

        page_name_txt = Label(text="Удаление авто", font=TITLE_FONT)
        page_name_txt.pack(pady=30)
        self.page_elements.append(page_name_txt)

        enter_vin = Label(self, text="Введите VIN авто", font=FONT)
        self.vin_field = Entry(self, font=FONT)

        elements = [enter_vin, self.vin_field]

        self.page_elements += elements

        [x.pack(pady=15) for x in elements]

        delete_car_btn = Button(self, text="Удалить авто из автопарка", font=FONT, command=self.deleteCar)
        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)

        delete_car_btn.pack(pady=10)
        back_btn.pack(pady=10)

    def deleteCar(self):
        car_info = self.vin_field.get().strip()

        if not car_info:
            tkinter.messagebox.showwarning(title="Внимательнее!", message="Поле должно быть заполнено!")
            return

        try:
            self.db.delete_car(car_info)
            tkinter.messagebox.showinfo(title="Успешно!", message="Машина успешно удалена!")
        except Exception as e:
            logging.error(f"Ошибка при удалении машины: {e}")
            tkinter.messagebox.showerror(title="Ошибка!",
                                         message="Не удалось удалить машину. Проверьте корректность данных.")