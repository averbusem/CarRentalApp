import logging
import os


class DatabaseErrorHandler:
    def __init__(self, log_file="database_errors.log"):
        self.log_file = log_file
        self._setup_logger()

    def _setup_logger(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w'):  # Create the file if it doesn't exist
                pass
        logging.basicConfig(
            filename=self.log_file,
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def log_error(self, message, exception):
        logging.error(f"{message}: {exception}")
        print(f"An error occurred: {message}. Check the log file for details.")
