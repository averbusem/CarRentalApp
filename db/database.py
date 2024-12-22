import psycopg2
import psycopg2.extras as extras

from .error_handler import DatabaseErrorHandler


class Database:
    def __init__(self, user: str, password: str):
        """
        Initialize database connection based on dynamic user credentials.
        :param user: Database username.
        :param password: Database password.
        """
        self.error_handler = DatabaseErrorHandler()
        self.config = {
            "dbname": "car_rental",
            "user": user,
            "password": password,
            "host": "localhost",
            "port": "5432",
        }

        try:
            self.connection = psycopg2.connect(**self.config)
            self.connection.autocommit = True  # Enable auto-commit
            print(f"Database connection successful (User: {user})")
        except Exception as e:
            self.error_handler.log_error("Database connection failed", e)
            raise

    def close_connection(self):
        """Close the database connection."""
        if self.connection:
            try:
                self.connection.close()
                print("Database connection closed")
            except Exception as e:
                self.error_handler.log_error("Failed to close database connection", e)

    # Функции для таблицы Customer ===========================================================
    def get_all_customers(self):
        """Retrieve all customers using get_all_customers() function."""
        query = "SELECT * FROM get_all_customers();"
        with self.connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def find_customer_by_passport_or_email(self, search_value):
        """Find customer by passport or email."""
        query = "SELECT * FROM find_customer_by_passport_or_email(%s);"
        with self.connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
            cursor.execute(query, (search_value,))
            return cursor.fetchall()

    def add_customer(self, passport_number, first_name, middle_name, last_name, email, phone_number):
        """Add a new customer."""
        print(
            f"Attempting to add: {passport_number}, {first_name}, {middle_name}, {last_name}, {email}, {phone_number}")
        query = "SELECT add_customer(%s, %s, %s, %s, %s, %s);"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (passport_number, first_name, middle_name, last_name, email, phone_number))

    def delete_customer_by_passport_or_email(self, search_value):
        """Delete a customer by passport or email."""
        query = "SELECT delete_customer_by_passport_or_email(%s);"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (search_value,))

    # Функции для таблицы Cars ===========================================================
    def get_all_cars(self):
        """Retrieve all cars using get_all_cars() function."""
        query = "SELECT * FROM get_all_cars();"
        with self.connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def get_all_available_cars(self):
        """Retrieve all available cars using get_all_available_cars() function."""
        query = "SELECT * FROM get_all_available_cars();"
        with self.connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def find_cars(self, brand_name: str, model_name: str):
        """Find cars by brand and model."""
        query = "SELECT * FROM find_cars(%s, %s);"
        with self.connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
            cursor.execute(query, (brand_name, model_name))
            return cursor.fetchall()

    def add_car(self, vin_car: str, registration_number: str, brand_name: str, model_name: str, color: str):
        """Add a new car."""
        print(f"Attempting to add car: {vin_car}, {registration_number}, {brand_name}, {model_name}, {color}")
        query = "SELECT add_car(%s, %s, %s, %s, %s);"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (vin_car, registration_number, brand_name, model_name, color))

    def delete_car(self, vin_car: str):
        """Delete a car by VIN."""
        query = "SELECT delete_car(%s);"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (vin_car,))

    # Функции для таблицы Bookings ===========================================================
    def get_all_bookings(self):
        """Retrieve all bookings using get_all_bookings() function."""
        query = "SELECT * FROM get_all_bookings();"
        with self.connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def get_active_bookings(self):
        """Retrieve active bookings using get_active_bookings() function."""
        query = "SELECT * FROM get_active_bookings();"
        with self.connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def create_booking(self, passport_number, vin_car, start_date, end_date):
        """Create a booking for a customer and update the car status to 'unavailable'."""
        query = "SELECT create_booking(%s, %s, %s, %s);"
        with self.connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
            cursor.execute(query, (passport_number, vin_car, start_date, end_date))

    def close_booking(self, passport_number, vin_car):
        """Close a booking by updating its status to 'completed' and the car status to 'available'."""
        query = "SELECT close_booking(%s, %s);"
        with self.connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
            cursor.execute(query, (passport_number, vin_car))

    def get_all_models(self):
        """Retrieve all cars using get_all_cars() function."""
        query = "SELECT * FROM get_all_models();"
        with self.connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def add_model(self, brand_name: str, model_name: str, eng_volume: str, power: str, trans: str, cost: str):
        """Add a new car."""
        print(f"Attempting to add model: {brand_name}, {model_name}, {eng_volume}, {power}, {trans}, {cost}")
        query = "SELECT add_new_model(%s, %s, %s, %s, %s, %s);"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (brand_name, model_name, eng_volume, power, trans, cost))

    def change_model_cost(self, brand_name: str, model_name: str, cost: str):
        query = "SELECT update_rental_cost(%s, %s, %s);"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (brand_name, model_name, cost))

    def insert_test_data(self):
        """Insert test data into the database by invoking the `insert_test_data` function."""
        query = "SELECT insert_test_data();"
        with self.connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
            cursor.execute(query)

    # Функции для очистки базы данных ===========================================================
    def clear_all_tables(self):
        """Clear all tables in the database by truncating them with CASCADE."""
        query = "SELECT clear_all_tables();"
        with self.connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
            cursor.execute(query)

    def clear_cars_table(self):
        """Clear the Cars table by deleting cars without active bookings."""
        query = "SELECT clear_cars_table();"
        with self.connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
            cursor.execute(query)

    def clear_customers_table(self):
        """Clear the Customers table by deleting customers without active bookings."""
        query = "SELECT clear_customers_table();"
        with self.connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
            cursor.execute(query)

    def clear_bookings_table(self):
        """Clear the Bookings table by deleting completed bookings."""
        query = "SELECT clear_bookings_table();"
        with self.connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
            cursor.execute(query)

    def delete_customer_fully(self, passport_number: str):
        """
        Deletes all data associated with a user in the Customers and Bookings tables.
        Raises an exception if the user has active bookings.

        :param passport_number: The passport number of the user to delete.
        """
        query = "SELECT delete_customer_fully(%s);"
        with self.connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
            cursor.execute(query, (passport_number,))