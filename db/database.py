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

    def close_connection(self):
        """Close the database connection."""
        if self.connection:
            try:
                self.connection.close()
                print("Database connection closed")
            except Exception as e:
                self.error_handler.log_error("Failed to close database connection", e)