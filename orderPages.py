from tkinter import *

from config import FONT
from basePage import BasePage

class PreOrdersPage(BasePage):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        from mainPage import MainPage
        self.set_previous_page(MainPage)

        self.valid_orders_btn = Button(self, text="Просмотр действующих заказов", font=FONT, command=self.showOrdersNow)
        self.all_orders_btn = Button(self, text="Просмотр всех заказов", font=FONT, command=self.showAllOrders)
        self.back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)

        self.name_txt = Label(text=f"Заказы", font=("Arial", 25))
        self.name_txt.pack(pady=40)

        elements = [self.valid_orders_btn, self.all_orders_btn, self.back_btn]

        self.page_elements += elements
        self.page_elements.append(self.name_txt)

        [x.pack(pady=20) for x in elements]

    def showOrdersNow(self, *args, **kwargs):
        self.clear_p()
        valid_orders_page = ValidOrdersPage(self.master)
        valid_orders_page.set_previous_page(PreOrdersPage)
        valid_orders_page.pack(expand=True, anchor="center")

    def showAllOrders(self, *args, **kwargs):
        self.clear_p()
        all_orders_page = AllOrdersPage(self.master)
        all_orders_page.set_previous_page(PreOrdersPage)
        all_orders_page.pack(expand=True, anchor="center")


class ValidOrdersPage(BasePage):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        page_name_txt = Label(self, text="Действующие заказы", font=("Arial", 25))
        page_name_txt.pack(pady=30)

        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)
        back_btn.pack()


class AllOrdersPage(BasePage):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        page_name_txt = Label(self, text="Все заказы", font=("Arial", 25))
        page_name_txt.pack(pady=30)

        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)
        back_btn.pack()


class NewOrderPage(BasePage):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        from mainPage import MainPage
        self.set_previous_page(MainPage)

        page_name_txt = Label(text="Создать новый заказ", font=("Arial", 25))
        page_name_txt.pack(pady=30)
        self.page_elements.append(page_name_txt)

        enter_passport = Label(self, text="Введите паспорт клиента", font=FONT)
        enter_car = Label(self, text="Введите VIN авто", font=FONT)
        enter_booking_start_date = Label(self, text="Введите дату начала бронирования", font=FONT)
        enter_booking_end_date = Label(self, text="Введите дату конца бронирования", font=FONT)



        self.name_field = Entry(self, font=FONT)
        self.car_field = Entry(self, font=FONT)
        self.booking_start_date = Entry(self, font=FONT)
        self.booking_end_date = Entry(self, font=FONT)

        elements = [enter_passport, self.name_field, enter_car, self.car_field, enter_booking_start_date,
                    self.booking_start_date, enter_booking_end_date, self.booking_end_date]

        self.page_elements += elements

        [x.pack(pady=8) for x in elements]

        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)
        back_btn.pack(pady=10)


class CloseOrderPage(BasePage):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        from mainPage import MainPage
        self.set_previous_page(MainPage)

        page_name_txt = Label(text="Закрыть заказ", font=("Arial", 25))
        page_name_txt.pack(pady=30)
        self.page_elements.append(page_name_txt)

        enter_car = Label(self, text="Введите VIN авто", font=FONT)
        enter_passport = Label(self, text="Введите паспорт клиента", font=FONT)

        self.name_field = Entry(self, font=FONT)
        self.car_field = Entry(self, font=FONT)

        elements = [enter_passport, self.name_field, enter_car, self.car_field]

        self.page_elements += elements

        [x.pack(pady=8) for x in elements]

        close_order = Button(self, text="Закрыть заказ", font=FONT, command=self.closeOrder)
        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)

        close_order.pack(pady=10)
        back_btn.pack(pady=10)

    #функция закрытия заказа
    def closeOrder(self):
        pass