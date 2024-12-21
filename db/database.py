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
        try:
            with self.connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            self.error_handler.log_error("Failed to fetch all customers", e)
            return []

    def find_customer_by_passport_or_email(self, search_value):
        """Find customer by passport or email."""
        query = "SELECT * FROM find_customer_by_passport_or_email(%s);"
        try:
            with self.connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
                cursor.execute(query, (search_value,))
                return cursor.fetchall()
        except Exception as e:
            self.error_handler.log_error(f"Failed to find customer with search_value: {search_value}", e)
            return []

    def add_customer(self, passport_number, first_name, middle_name, last_name, email, phone_number):
        """Add a new customer."""
        print(
            f"Attempting to add: {passport_number}, {first_name}, {middle_name}, {last_name}, {email}, {phone_number}")
        query = "SELECT add_customer(%s, %s, %s, %s, %s, %s);"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (passport_number, first_name, middle_name, last_name, email, phone_number))
                print("Customer added successfully")
        except Exception as e:
            self.error_handler.log_error(f"Failed to add customer {passport_number}", e)

    def delete_customer_by_passport_or_email(self, search_value):
        """Delete a customer by passport or email."""
        query = "SELECT delete_customer_by_passport_or_email(%s);"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (search_value,))
                print("Customer deleted successfully")
        except Exception as e:
            self.error_handler.log_error(f"Failed to delete customer with search_value: {search_value}", e)

    # Функции для таблицы Cars ===========================================================
    def get_all_cars(self):
        """Retrieve all cars using get_all_cars() function."""
        query = "SELECT * FROM get_all_cars();"
        try:
            with self.connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            self.error_handler.log_error("Failed to get all cars", e)
            return []

    def get_all_available_cars(self):
        """Retrieve all available cars using get_all_available_cars() function."""
        query = "SELECT * FROM get_all_available_cars();"
        try:
            with self.connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            self.error_handler.log_error("Failed to get available cars", e)
            return []

    def find_cars(self, brand_name: str, model_name: str):
        """Find cars by brand and model."""
        query = "SELECT * FROM find_cars(%s, %s);"
        try:
            with self.connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
                cursor.execute(query, (brand_name, model_name))
                return cursor.fetchall()
        except Exception as e:
            self.error_handler.log_error(f"Failed to find cars: {brand_name} {model_name}", e)
            return []

    def add_car(self, vin_car: str, registration_number: str, brand_name: str, model_name: str, color: str):
        """Add a new car."""
        print(f"Attempting to add car: {vin_car}, {registration_number}, {brand_name}, {model_name}, {color}")
        query = "SELECT add_car(%s, %s, %s, %s, %s);"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (vin_car, registration_number, brand_name, model_name, color))
                print("Car added successfully")
        except Exception as e:
            self.error_handler.log_error(f"Failed to add car {vin_car}", e)

    def delete_car(self, vin_car: str):
        """Delete a car by VIN."""
        query = "SELECT delete_car(%s);"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (vin_car,))
                print("Car deleted successfully")
        except Exception as e:
            self.error_handler.log_error(f"Failed to delete car with VIN: {vin_car}", e)

    # Функции для таблицы Bookings ===========================================================
    def get_all_bookings(self):
        """Retrieve all bookings using get_all_bookings() function."""
        query = "SELECT * FROM get_all_bookings();"
        try:
            with self.connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            self.error_handler.log_error("Failed to fetch all bookings", e)
            return []

    def get_active_bookings(self):
        """Retrieve active bookings using get_active_bookings() function."""
        query = "SELECT * FROM get_active_bookings();"
        try:
            with self.connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            self.error_handler.log_error("Failed to fetch active bookings", e)
            return []

    def create_booking(self, passport_number, vin_car, start_date, end_date):
        """Create a booking for a customer and update the car status to 'unavailable'."""
        query = "SELECT create_booking(%s, %s, %s, %s);"
        try:
            with self.connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
                cursor.execute(query, (passport_number, vin_car, start_date, end_date))
                print(f"Booking created successfully for {passport_number} with car {vin_car}")
        except Exception as e:
            self.error_handler.log_error(f"Failed to create booking for {passport_number} with car {vin_car}", e)

    def close_booking(self, passport_number, vin_car):
        """Close a booking by updating its status to 'completed' and the car status to 'available'."""
        query = "SELECT close_booking(%s, %s);"
        try:
            with self.connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
                cursor.execute(query, (passport_number, vin_car))
                print(f"Booking closed successfully for {passport_number} with car {vin_car}")
        except Exception as e:
            self.error_handler.log_error(f"Failed to close booking for {passport_number} with car {vin_car}", e)

    def get_all_models(self):
        """Retrieve all cars using get_all_cars() function."""
        query = "SELECT * FROM get_all_models();"
        try:
            with self.connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            self.error_handler.log_error("Failed to get all models", e)
            return []

    def find_model(self, brand_name: str, model_name: str):
        """Find cars by brand and model."""
        query = "SELECT * FROM find_model_by_brand_and_name(%s, %s);"
        try:
            with self.connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
                cursor.execute(query, (brand_name, model_name))
                return cursor.fetchall()
        except Exception as e:
            self.error_handler.log_error(f"Failed to find model: {brand_name} {model_name}", e)
            return []

    def add_model(self, brand_name: str, model_name: str, eng_volume: str, power: str, trans: str, cost: str):
        """Add a new car."""
        print(f"Attempting to add model: {brand_name}, {model_name}, {eng_volume}, {power}, {trans}, {cost}")
        query = "SELECT add_new_model(%s, %s, %s, %s, %s, %s);"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (brand_name, model_name, eng_volume, power, trans, cost))
                print("Model added successfully")
        except Exception as e:
            self.error_handler.log_error(f"Failed to add model {brand_name} {model_name}", e)

    def delete_model(self, brand_name: str, model_name: str):
        """Delete a car by VIN."""
        query = "SELECT delete_model(%s, %s);"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (brand_name, model_name))
                print("Model deleted successfully")
        except Exception as e:
            self.error_handler.log_error(f"Failed to delete model: {brand_name} {model_name}", e)

    def change_model_cost(self, brand_name: str, model_name: str, cost: str):
        """Delete a car by VIN."""
        query = "SELECT update_rental_cost(%s, %s, %s);"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (brand_name, model_name, cost))
                print("Model cost modified successfully")
        except Exception as e:
            self.error_handler.log_error(f"Failed to change cost of model: {brand_name} {model_name} {cost}", e)