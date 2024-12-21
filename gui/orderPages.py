import logging
import tkinter
from tkinter import *
from tkinter import messagebox

from gui.basePage import BasePage
from gui.config import FONT, TITLE_FONT


class PreOrdersPage(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, db, *args, **kwargs)

        from gui.mainPage import MainPage
        self.set_previous_page(MainPage)


        self.create_order_btn = Button(self, text="Создать заказ", font=FONT, command=self.goToNewOrder, width=27)
        self.close_order_btn = Button(self, text="Закрыть заказ", font=FONT, command=self.goToClosingOrder, width=27)
        self.valid_orders_btn = Button(self, text="Просмотр действующих заказов", font=FONT, command=self.showOrdersNow, width=27)
        self.all_orders_btn = Button(self, text="Просмотр всех заказов", font=FONT, command=self.showAllOrders, width=27)
        self.back_btn = Button(self, text="Назад", font=FONT, command=self.goBack, width=10)

        self.name_txt = Label(text=f"Заказы", font=TITLE_FONT)
        self.name_txt.pack(pady=40)

        elements = [self.create_order_btn, self.close_order_btn, self.valid_orders_btn, self.all_orders_btn,
                    self.back_btn]

        self.page_elements += elements
        self.page_elements.append(self.name_txt)

        [x.pack(pady=20) for x in elements]

    def goToNewOrder(self, *args, **kwargs):
        self.clear_p()
        new_order_p = NewOrderPage(self.master, self.db)  # Передаем db в NewOrderPage
        new_order_p.pack(expand=True, anchor='center')

    def goToClosingOrder(self, *args, **kwargs):
        self.clear_p()
        close_order_p = CloseOrderPage(self.master, self.db)  # Передаем db
        close_order_p.pack(expand=True, anchor='center')

    def showOrdersNow(self, *args, **kwargs):
        self.clear_p()
        valid_orders_page = ValidOrdersPage(self.master, self.db)  # Передаем db в ValidOrdersPage
        valid_orders_page.set_previous_page(PreOrdersPage)
        valid_orders_page.pack(expand=True, anchor="center")

    def showAllOrders(self, *args, **kwargs):
        self.clear_p()
        all_orders_page = AllOrdersPage(self.master, self.db)  # Передаем db в AllOrdersPage
        all_orders_page.set_previous_page(PreOrdersPage)
        all_orders_page.pack(expand=True, anchor="center")

class ValidOrdersPage(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, db, *args, **kwargs)
        self.set_previous_page(PreOrdersPage)

        page_name_txt = Label(self, text="Действующие заказы", font=TITLE_FONT)
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

        # Загрузка данных о всех заказах
        self.load_active_orders()

        # Настройка прокрутки
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)
        back_btn.pack(pady=20)

    def load_active_orders(self):
        # Получаем список всех заказов
        active_orders = self.db.get_active_bookings()
        if not active_orders:
            no_data_label = Label(self.inner_frame, text="Нет активных заказов.", font=FONT)
            no_data_label.pack(pady=10)
            return

        # Отображение информации о свободных автомобилях
        for i, order in enumerate(active_orders, start=1):
            order_info = (f"{i}. {order['passport_number']} - {order['vin_car']} - {order['start_date']} - {order['end_date']} - "
                        f"{order['cost']} - {order['booking_status']}")
            order_label = Label(self.inner_frame, text=order_info, font=FONT, anchor="w", justify="left")
            order_label.pack(fill="x", padx=10, pady=5)

    def _on_mouse_wheel(self, event):
        """Обрабатывает прокрутку колесиком мыши."""
        if event.state == 0:  # Прокрутка вертикальная
            self.canvas.yview_scroll(-1 * (event.delta // 120), "units")
        elif event.state == 1:  # Прокрутка горизонтальная (при удержании Shift)
            self.canvas.xview_scroll(-1 * (event.delta // 120), "units")


class AllOrdersPage(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, db, *args, **kwargs)
        self.set_previous_page(PreOrdersPage)

        page_name_txt = Label(self, text="Все заказы", font=TITLE_FONT)
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

        # Загрузка данных о всех заказах
        self.load_all_orders()

        # Настройка прокрутки
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)
        back_btn.pack(pady=20)

    def load_all_orders(self):
        # Получаем список всех заказов
        all_orders = self.db.get_all_bookings()
        if not all_orders:
            no_data_label = Label(self.inner_frame, text="Заказов еще не было.", font=FONT)
            no_data_label.pack(pady=10)
            return

        # Отображение информации о свободных автомобилях
        for i, order in enumerate(all_orders, start=1):
            order_info = (f"{i}. {order['passport_number']} - {order['vin_car']} - {order['start_date']} - {order['end_date']} - "
                        f"{order['cost']} - {order['booking_status']}")
            order_label = Label(self.inner_frame, text=order_info, font=FONT, anchor="w", justify="left")
            order_label.pack(fill="x", padx=10, pady=5)

    def _on_mouse_wheel(self, event):
        """Обрабатывает прокрутку колесиком мыши."""
        if event.state == 0:  # Прокрутка вертикальная
            self.canvas.yview_scroll(-1 * (event.delta // 120), "units")
        elif event.state == 1:  # Прокрутка горизонтальная (при удержании Shift)
            self.canvas.xview_scroll(-1 * (event.delta // 120), "units")

class NewOrderPage(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, db, *args, **kwargs)
        self.set_previous_page(PreOrdersPage)

        page_name_txt = Label(text="Создать новый заказ", font=TITLE_FONT)
        page_name_txt.pack(pady=30)
        self.page_elements.append(page_name_txt)

        enter_passport = Label(self, text="Введите паспорт клиента (10 цифр)", font=FONT)
        enter_car = Label(self, text="Введите VIN авто (17 цифр)", font=FONT)
        enter_booking_start_date = Label(self, text="Введите дату начала бронирования (в формате DD.MM.YYYY)", font=FONT)
        enter_booking_end_date = Label(self, text="Введите дату конца бронирования (в формате DD.MM.YYYY)", font=FONT)

        self.name_field = Entry(self, font=FONT)
        self.car_field = Entry(self, font=FONT)
        self.booking_start_date = Entry(self, font=FONT)
        self.booking_end_date = Entry(self, font=FONT)

        elements = [enter_passport, self.name_field, enter_car, self.car_field, enter_booking_start_date,
                    self.booking_start_date, enter_booking_end_date, self.booking_end_date]

        self.page_elements += elements

        [x.pack(pady=8) for x in elements]

        create_order_btn = Button(self, text="Создать заказ", font=FONT, command=self.createOrder)
        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)

        create_order_btn.pack(pady=10)
        back_btn.pack(pady=10)

    #функция создания заказа
    def createOrder(self):
        order_info = [
            self.name_field.get().strip(),
            self.car_field.get().strip(),
            self.booking_start_date.get().strip(),
            self.booking_end_date.get().strip()
        ]

        if not (order_info[0].isdigit() and len(order_info[0]) == 10 and # паспорт - число и длина равна 10
                len(order_info[1]) == 17 and # VIN - длина равна 17
                # добавить логику обработки дат
                all(field for field in order_info)):
            tkinter.messagebox.showwarning(title="Внимательнее", message="Все поля должны быть заполнены правильно!")
            return

        try:
            self.db.create_booking(order_info[0], order_info[1], order_info[2], order_info[3])
            tkinter.messagebox.showinfo(title="Успешно!", message="Заказ успешно создан!")
        except Exception as e:
            logging.error(f"Ошибка при создании заказа: {e}")
            tkinter.messagebox.showerror(title="Ошибка!", message="Не удалось создать заказ. Проверьте корректность данных.")


class CloseOrderPage(BasePage):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, db,*args, **kwargs)
        self.set_previous_page(PreOrdersPage)

        page_name_txt = Label(text="Закрыть заказ", font=TITLE_FONT)
        page_name_txt.pack(pady=30)
        self.page_elements.append(page_name_txt)

        enter_passport = Label(self, text="Введите паспорт клиента", font=FONT)
        enter_car = Label(self, text="Введите VIN авто", font=FONT)

        self.pass_field = Entry(self, font=FONT)
        self.car_field = Entry(self, font=FONT)

        elements = [enter_passport, self.pass_field, enter_car, self.car_field]

        self.page_elements += elements

        [x.pack(pady=8) for x in elements]

        close_order = Button(self, text="Закрыть заказ", font=FONT, command=self.closeOrder)
        back_btn = Button(self, text="Назад", font=FONT, command=self.goBack)

        close_order.pack(pady=10)
        back_btn.pack(pady=10)

    #функция закрытия заказа
    def closeOrder(self):
        order_info = [self.pass_field.get().strip(), self.car_field.get().strip()]

        if not (order_info[0].isdigit() and len(order_info[0]) == 10 and # паспорт - число длиной 10
                len(order_info[1]) == 17 and # VIN - длиной 17
                all(field for field in order_info)):
            tkinter.messagebox.showwarning(title="Внимательнее", message="Все поля должны быть заполнены правильно!")
            return

        try:
            self.db.close_booking(order_info[0], order_info[1])
            tkinter.messagebox.showinfo(title="Успешно!", message="Заказ успешно закрыт!")
        except Exception as e:
            logging.error(f"Ошибка при закрытии заказа: {e}")
            tkinter.messagebox.showerror(title="Ошибка!", message="Не удалось закрыть заказ. Проверьте корректность данных.")