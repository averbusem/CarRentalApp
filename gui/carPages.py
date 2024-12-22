import logging
import re
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

        self.cars_page_btn = Button(self, text="Работа с авто", font=FONT, command=self.goToCars, width=23)
        self.models_page_btn = Button(self, text="Работа с моделями авто", font=FONT, command=self.goToModels, width=23)

        self.back_btn = Button(self, text="Назад", font=FONT, command=self.goBack, width=10)

        self.name_txt = Label(text=f"Автопарк", font=TITLE_FONT)
        self.name_txt.pack(pady=40)

        elements = [self.cars_page_btn, self.models_page_btn, self.back_btn]

        self.page_elements += elements
        self.page_elements.append(self.name_txt)

        [x.pack(pady=20) for x in elements]

    def goToCars(self, *args, **kwargs):
        self.clear_p()
        cars_p = CarsPage(self.master, self.db)
        cars_p.pack(expand=True, anchor="center")

    def goToModels(self, *args, **kwargs):
        self.clear_p()
        models_p = ModelsPage(self.master, self.db)
        models_p.pack(expand=True, anchor="center")


class CarsPage(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, db, *args, **kwargs)

        self.set_previous_page(PreCarsPage)
        self.all_cars_btn = Button(self, text="Просмотр всех машин", font=FONT, command=self.listOfCars, width=27)
        self.free_cars_btn = Button(self, text="Просмотр свободных машин", font=FONT, command=self.checkFreeCars,
                                    width=27)
        self.find_car_btn = Button(self, text="Найти авто", font=FONT, command=self.findCar, width=27)
        self.add_car_btn = Button(self, text="Добавить авто", font=FONT, command=self.addCar, width=27)
        self.delete_car_btn = Button(self, text="Удалить машину из автопарка", font=FONT, command=self.deleteCar,
                                     width=27)
        self.back_btn = Button(self, text="Назад", font=FONT, command=self.goBack, width=10)

        self.name_txt = Label(text=f"Автопарк (автомобили)", font=TITLE_FONT)
        self.name_txt.pack(pady=40)

        elements = [self.all_cars_btn, self.free_cars_btn, self.find_car_btn, self.add_car_btn, self.delete_car_btn,
                    self.back_btn]

        self.page_elements += elements
        self.page_elements.append(self.name_txt)

        [x.pack(pady=20) for x in elements]

    def listOfCars(self, *args, **kwargs):
        self.clear_p()
        all_cars_page = AllCarsPage(self.master, db=self.db)
        all_cars_page.pack(expand=True, anchor="center")

    def checkFreeCars(self, *args, **kwargs):
        self.clear_p()
        free_cars_page = FreeCarsPage(self.master, db=self.db)
        free_cars_page.pack(expand=True, anchor="center")

    def findCar(self, *args, **kwargs):
        self.clear_p()
        find_car_page = FindCarPage(self.master, db=self.db)
        find_car_page.pack(expand=True, anchor="center")

    def addCar(self, *args, **kwargs):
        self.clear_p()
        add_car_page = AddCarPage(self.master, db=self.db)
        add_car_page.pack(expand=True, anchor="center")

    def deleteCar(self, *args, **kwargs):
        self.clear_p()
        delete_car_page = DeleteCarPage(self.master, db=self.db)
        delete_car_page.pack(expand=True, anchor="center")


class ModelsPage(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, db, *args, **kwargs)
        self.set_previous_page(PreCarsPage)

        self.all_models_btn = Button(self, text="Просмотр всех моделей", font=FONT, command=self.allModels, width=25)
        self.add_model_btn = Button(self, text="Добавить модель", font=FONT, command=self.addModel, width=25)
        self.change_price_btn = Button(self, text="Изменить стоимость модели", font=FONT, command=self.changePrice, width=25)

        self.back_btn = Button(self, text="Назад", font=FONT, command=self.goBack, width=10)

        self.name_txt = Label(text=f"Автопарк (модели)", font=TITLE_FONT)
        self.name_txt.pack(pady=40)

        elements = [self.all_models_btn, self.add_model_btn, self.change_price_btn, self.back_btn]

        self.page_elements += elements
        self.page_elements.append(self.name_txt)

        [x.pack(pady=20) for x in elements]

    def allModels(self, *args, **kwargs):
        self.clear_p()
        all_models_page = AllModelsPage(self.master, db=self.db)
        all_models_page.pack(expand=True, anchor="center")

    def addModel(self, *args, **kwargs):
        self.clear_p()
        add_model_p = AddModelPage(self.master, db=self.db)
        add_model_p.pack(expand=True, anchor="center")

    def changePrice(self, *args, **kwargs):
        self.clear_p()
        change_price_p = ChangePricePage(self.master, db=self.db)
        change_price_p.pack(expand=True, anchor="center")


class AllCarsPage(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, db, *args, **kwargs)
        self.set_previous_page(CarsPage)

        page_name_txt = Label(self, text="Просмотр всех авто", font=TITLE_FONT)
        page_name_txt.pack(pady=30)

        # Обертка для прокручиваемой области
        self.scroll_frame = Frame(self)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Canvas для прокрутки
        self.canvas = Canvas(self.scroll_frame, width=self.master.winfo_screenwidth() // 2,
                             height=self.master.winfo_screenheight() // 2.5)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Вертикальный Scrollbar
        self.v_scrollbar = Scrollbar(self.scroll_frame, orient="vertical", command=self.canvas.yview)
        self.v_scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)

        # Горизонтальный Scrollbar
        self.h_scrollbar = Scrollbar(self.scroll_frame, orient="horizontal", command=self.canvas.xview)
        self.h_scrollbar.pack(side="bottom", fill="x")
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set)

        # Внутренний Frame для размещения содержимого
        self.inner_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Загрузка данных авто
        self.load_cars()

        # Настройка прокрутки
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)
        back_btn.pack(pady=20)

    def load_cars(self):
        cars = self.db.get_all_cars()
        if not cars:
            no_data_label = Label(self.inner_frame, text="Нет данных об автомобилях.", font=FONT)
            no_data_label.pack(pady=10)
            return

        # Создаем текстовый виджет для отображения списка автомобилей
        car_text = Text(self.inner_frame, font=FONT, wrap="word", bg=self["bg"], bd=0, highlightthickness=0, height=15)

        # Добавляем информацию об автомобилях в виджет
        for i, car in enumerate(cars, start=1):
            car_info = (f"{i}. {car['vin_car']} - {car['brand_name']} - {car['model_name']} - {car['rental_cost']} - "
                        f"{car['registration_number']} - {car['color']} - {car['car_status']} - {car['engine_volume']} - "
                        f"{car['horsepower']} - {car['transmission']}\n")
            car_text.insert("end", car_info)

        car_text.config(state="disabled")  # Делаем виджет только для чтения
        car_text.pack(fill="x", padx=10, pady=5)

    def _on_mouse_wheel(self, event):
        """Обрабатывает прокрутку колесиком мыши."""
        if event.state == 0:  # Прокрутка вертикальная
            self.canvas.yview_scroll(-1 * (event.delta // 120), "units")
        elif event.state == 1:  # Прокрутка горизонтальная (при удержании Shift)
            self.canvas.xview_scroll(-1 * (event.delta // 120), "units")


class FreeCarsPage(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, db, *args, **kwargs)
        self.set_previous_page(CarsPage)

        page_name_txt = Label(self, text="Свободные автомобили", font=TITLE_FONT)
        page_name_txt.pack(pady=30)

        # Обертка для прокручиваемой области
        self.scroll_frame = Frame(self)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Canvas для прокрутки
        self.canvas = Canvas(self.scroll_frame, width=self.master.winfo_screenwidth() // 2,
                             height=self.master.winfo_screenheight() // 2.5)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Вертикальный Scrollbar
        self.v_scrollbar = Scrollbar(self.scroll_frame, orient="vertical", command=self.canvas.yview)
        self.v_scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)

        # Горизонтальный Scrollbar
        self.h_scrollbar = Scrollbar(self.scroll_frame, orient="horizontal", command=self.canvas.xview)
        self.h_scrollbar.pack(side="bottom", fill="x")
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set)

        # Внутренний Frame для размещения содержимого
        self.inner_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Загрузка данных о свободных автомобилях
        self.load_free_cars()

        # Настройка прокрутки
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)
        back_btn.pack(pady=20)

    def load_free_cars(self):
        # Получаем список свободных автомобилей
        free_cars = self.db.get_all_available_cars()
        if not free_cars:
            no_data_label = Label(self.inner_frame, text="Нет свободных автомобилей.", font=FONT)
            no_data_label.pack(pady=10)
            return

        # Создаем виджет Text для отображения информации
        car_text = Text(self.inner_frame, font=FONT, wrap="word", bg=self["bg"], bd=0, highlightthickness=0, height=15)

        # Добавляем информацию о свободных автомобилях в виджет
        for i, car in enumerate(free_cars, start=1):
            car_info = (f"{i}. {car['vin_car']} - {car['brand_name']} - {car['model_name']} - {car['rental_cost']} - "
                        f"{car['registration_number']} - {car['color']} - {car['car_status']} - {car['engine_volume']} - "
                        f"{car['horsepower']} - {car['transmission']}\n")
            car_text.insert("end", car_info)

        car_text.config(state="disabled")  # Делаем виджет только для чтения

        # Добавляем прокрутку, если список автомобилей длинный
        scrollbar = Scrollbar(self.inner_frame, command=car_text.yview)
        car_text.config(yscrollcommand=scrollbar.set)

        # Размещение виджетов
        scrollbar.pack(side="right", fill="y")
        car_text.pack(fill="both", padx=10, pady=5)

    def _on_mouse_wheel(self, event):
        """Обрабатывает прокрутку колесиком мыши."""
        if event.state == 0:  # Прокрутка вертикальная
            self.canvas.yview_scroll(-1 * (event.delta // 120), "units")
        elif event.state == 1:  # Прокрутка горизонтальная (при удержании Shift)
            self.canvas.xview_scroll(-1 * (event.delta // 120), "units")


class FindCarPage(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, db, *args, **kwargs)
        self.set_previous_page(CarsPage)
        page_name_txt = Label(self, text="Найти авто", font=TITLE_FONT)
        page_name_txt.pack(pady=30)

        enter_brand = Label(self, text="Введите марку машин", font=FONT)
        enter_model = Label(self, text="Введите модель машин", font=FONT)

        self.brand_field = Entry(self, font=FONT)
        self.model_field = Entry(self, font=FONT)

        elements = [enter_brand, self.brand_field, enter_model, self.model_field]

        self.page_elements += elements

        [x.pack(pady=10) for x in elements]

        find_btn = Button(self, text="Найти", font=FONT, command=self.findCars)
        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)

        find_btn.pack(pady=15)
        back_btn.pack(pady=15)

    def findCars(self, *args, **kwargs):
        car_info = [self.brand_field.get().strip(), self.model_field.get().strip()]
        if car_info[0].isalpha() and car_info[1].isalpha():
            self.clear_p()
            found_cars_page = CarsBySearching(self.master, db=self.db, brand=car_info[0], model=car_info[1])
            found_cars_page.pack(expand=True, anchor="center")
        else:
            tkinter.messagebox.showwarning(title="Внимательнее", message="Все поля должны быть заполнены правильно!")
            return


class CarsBySearching(BasePage):
    def __init__(self, master, db, brand, model, *args, **kwargs):
        super().__init__(master, db, *args, **kwargs)
        self.set_previous_page(CarsPage)

        page_name_txt = Label(self, text="Найденные авто", font=TITLE_FONT)
        page_name_txt.pack(pady=30)

        # Обертка для прокручиваемой области
        self.scroll_frame = Frame(self)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Canvas для прокрутки
        self.canvas = Canvas(self.scroll_frame, width=self.master.winfo_screenwidth() // 2,
                             height=self.master.winfo_screenheight() // 2.5)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Вертикальный Scrollbar
        self.v_scrollbar = Scrollbar(self.scroll_frame, orient="vertical", command=self.canvas.yview)
        self.v_scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)

        # Горизонтальный Scrollbar
        self.h_scrollbar = Scrollbar(self.scroll_frame, orient="horizontal", command=self.canvas.xview)
        self.h_scrollbar.pack(side="bottom", fill="x")
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set)

        # Внутренний Frame для размещения содержимого
        self.inner_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Загрузка данных о свободных автомобилях
        self.load_found_cars(brand, model)

        # Настройка прокрутки
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)
        back_btn.pack(pady=20)

    def load_found_cars(self, brand: str, model: str):
        # Получаем список автомобилей
        cars = self.db.find_cars(brand, model)
        if not cars:
            no_data_label = Label(self.inner_frame, text="Нет автомобилей такой модели.", font=FONT)
            no_data_label.pack(pady=10)
            return

        # Создаем виджет Text для отображения информации
        car_text = Text(self.inner_frame, font=FONT, wrap="word", bg=self["bg"], bd=0, highlightthickness=0, height=15)

        # Добавляем информацию о найденных автомобилях в виджет
        for i, car in enumerate(cars, start=1):
            car_info = (f"{i}. {car['vin_car']} - {car['brand_name']} - {car['model_name']} - {car['rental_cost']} - "
                        f"{car['registration_number']} - {car['color']} - {car['car_status']} - {car['engine_volume']} - "
                        f"{car['horsepower']} - {car['transmission']}\n")
            car_text.insert("end", car_info)

        car_text.config(state="disabled")  # Делаем виджет только для чтения

        # Добавляем прокрутку, если список автомобилей длинный
        scrollbar = Scrollbar(self.inner_frame, command=car_text.yview)
        car_text.config(yscrollcommand=scrollbar.set)

        # Размещение виджетов
        scrollbar.pack(side="right", fill="y")
        car_text.pack(fill="both", padx=10, pady=5)

    def _on_mouse_wheel(self, event):
        """Обрабатывает прокрутку колесиком мыши."""
        if event.state == 0:  # Прокрутка вертикальная
            self.canvas.yview_scroll(-1 * (event.delta // 120), "units")
        elif event.state == 1:  # Прокрутка горизонтальная (при удержании Shift)
            self.canvas.xview_scroll(-1 * (event.delta // 120), "units")


class AddCarPage(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, db, *args, **kwargs)
        self.set_previous_page(CarsPage)

        page_name_txt = Label(text="Добавление авто", font=TITLE_FONT)
        page_name_txt.pack(pady=30)
        self.page_elements.append(page_name_txt)

        enter_vin = Label(self, text="Введите VIN авто (17 знаков)", font=FONT)
        enter_number = Label(self, text="Введите гос номер авто (в формате А123АА)", font=FONT)
        enter_brand = Label(self, text="Введите марку авто", font=FONT)
        enter_model = Label(self, text="Введите модель авто", font=FONT)
        enter_color = Label(self, text="Введите цвет машины (например, красный)", font=FONT)

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

        if not (len(car_info[0]) == 17 and # если длина VIN  17
                len(car_info[1]) in {8, 9} and car_info[1][1:4].isdigit() and car_info[1][0].isalpha() and car_info[1][4:6].isalpha() and # если номер соответствует А123АА52 или А123АА152
                len(car_info[2]) > 0 and len(car_info[3]) > 0 and len(car_info[4]) > 0 and car_info[4].isalpha() and  # если марка и модель - не числа
                all(field for field in car_info)): #если не заполненны все поля
            tkinter.messagebox.showwarning(title="Внимательнее", message="Все поля должны быть заполнены правильно!")
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
        self.set_previous_page(ModelsPage)

        page_name_txt = Label(text="Добавление модели авто", font=TITLE_FONT)
        page_name_txt.pack(pady=30)
        self.page_elements.append(page_name_txt)

        enter_brand = Label(self, text="Введите марку", font=FONT)
        enter_model_name = Label(self, text="Введите название модели", font=FONT)
        enter_eng_volume = Label(self, text="Введите объём двигателя (например, 5.0)", font=FONT)
        enter_h_power = Label(self, text="Введите лошадинные силы авто", font=FONT)
        enter_transmission = Label(self, text="Введите КПП модели авто (мех, авто, робот)", font=FONT)
        enter_price = Label(self, text="Введите стоимость за день проката (например, 150.25)", font=FONT)

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

        # ОБНОВИТЬ ЛОГИКУ ПРОВЕРКИ ЦЕНЫ. СЕЙЧАС ОШИБКА В ДОБАВЛЕНИИ ИЗ-ЗА NUMERIC ТИПА В SQL

        if not (len(model_info[0]) > 0 and len(model_info[1]) > 0 and
                model_info[3].isdigit() and model_info[4].isalpha() and # если объём двигателя и мощность - числа
                all(field for field in model_info)): # если заполнены все поля
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
        self.set_previous_page(CarsPage)

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

        if not (len(car_info) == 17 and car_info): # если длина VIN равна 17 и не пустая ячейка
            tkinter.messagebox.showwarning(title="Внимательнее!", message="Поле должно быть заполнено правильно!")
            return

        try:
            self.db.delete_car(car_info)
            tkinter.messagebox.showinfo(title="Успешно!", message="Машина успешно удалена!")
        except Exception as e:
            logging.error(f"Ошибка при удалении машины: {e}")
            tkinter.messagebox.showerror(title="Ошибка!",
                                         message="Не удалось удалить машину. Проверьте корректность данных.")

class ChangePricePage(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, db, *args, **kwargs)
        self.set_previous_page(ModelsPage)

        page_name_txt = Label(self, text="Изменение цены аренды", font=TITLE_FONT)
        page_name_txt.pack(pady=30)

        # Метки и поля ввода
        enter_brand = Label(self, text="Введите марку авто:", font=FONT)
        enter_model = Label(self, text="Введите модель авто:", font=FONT)
        enter_price = Label(self, text="Введите новую стоимость аренды:", font=FONT)

        self.brand_field = Entry(self, font=FONT)
        self.model_field = Entry(self, font=FONT)
        self.price_field = Entry(self, font=FONT)

        elements = [enter_brand, self.brand_field, enter_model, self.model_field, enter_price, self.price_field]

        self.page_elements += elements

        [x.pack(pady=10) for x in elements]

        change_price_btn = Button(self, text="Изменить стоимость аренды авто", font=FONT, command=self.changePrice)
        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)

        change_price_btn.pack(pady=10)
        back_btn.pack(pady=10)

    def changePrice(self):
        info = [self.brand_field.get().strip(), self.model_field.get().strip(), self.price_field.get().strip()]

        # Проверка на заполненность полей
        if not info[0] or not info[1] or not info[2]:
            tkinter.messagebox.showwarning(title="Внимание!", message="Все поля должны быть заполнены!")
            return

        # Проверка корректности ввода цены
        if not (re.match(r"[+-]?([0-9]*[.])?[0-9]+", info[2]) and float(info[2]) >= 0):
            tkinter.messagebox.showerror(title="Ошибка!", message="Цена должна быть положительным числом!")
            return

        try:
            # Обновление цены в базе данных
            self.db.change_model_cost(brand_name=info[0], model_name=info[1], cost=info[2])
            tkinter.messagebox.showinfo(title="Успешно!", message="Стоимость аренды успешно обновлена!")
        except Exception as e:
            logging.error(f"Ошибка при обновлении цены аренды: {e}")
            tkinter.messagebox.showerror(title="Ошибка!", message="Не удалось обновить цену. Проверьте корректность данных.")

class AllModelsPage(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, db, *args, **kwargs)
        self.set_previous_page(ModelsPage)

        page_name_txt = Label(self, text="Просмотр всех моделей", font=TITLE_FONT)
        page_name_txt.pack(pady=30)

        # Обертка для прокручиваемой области
        self.scroll_frame = Frame(self)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Canvas для прокрутки
        self.canvas = Canvas(self.scroll_frame, width=self.master.winfo_screenwidth() // 2,
                             height=self.master.winfo_screenheight() // 2.5)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Вертикальный Scrollbar
        self.v_scrollbar = Scrollbar(self.scroll_frame, orient="vertical", command=self.canvas.yview)
        self.v_scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)

        # Горизонтальный Scrollbar
        self.h_scrollbar = Scrollbar(self.scroll_frame, orient="horizontal", command=self.canvas.xview)
        self.h_scrollbar.pack(side="bottom", fill="x")
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set)

        # Внутренний Frame для размещения содержимого
        self.inner_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Загрузка данных авто
        self.load_models()

        # Настройка прокрутки
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)
        back_btn.pack(pady=20)

    def load_models(self):
        models = self.db.get_all_models()
        if not models:
            no_data_label = Label(self.inner_frame, text="Нет данных о моделях.", font=FONT)
            no_data_label.pack(pady=10)
            return

        # Создаем виджет Text для отображения информации
        models_text = Text(self.inner_frame, font=FONT, wrap="word", bg=self["bg"], bd=0, highlightthickness=0, height=15)

        # Добавляем информацию о моделях в Text
        for i, model in enumerate(models, start=1):
            model_info = (f"{i}. {model['brand_name']} - {model['model_name']} - {model['engine_volume']} - "
                          f"{model['horsepower']} - {model['transmission']} - {model['rental_cost']}\n")
            models_text.insert("end", model_info)

        models_text.config(state="disabled")  # Делаем Text только для чтения

        # Добавляем прокрутку
        scrollbar = Scrollbar(self.inner_frame, command=models_text.yview)
        models_text.config(yscrollcommand=scrollbar.set)

        # Размещение виджетов
        scrollbar.pack(side="right", fill="y")
        models_text.pack(fill="both", padx=10, pady=5)

    def _on_mouse_wheel(self, event):
        """Обрабатывает прокрутку колесиком мыши."""
        if event.state == 0:  # Прокрутка вертикальная
            self.canvas.yview_scroll(-1 * (event.delta // 120), "units")
        elif event.state == 1:  # Прокрутка горизонтальная (при удержании Shift)
            self.canvas.xview_scroll(-1 * (event.delta // 120), "units")
