import logging
from logging.handlers import RotatingFileHandler
from flask import request

class BlogLog:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(BlogLog, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self):
        # Configure the logger
        self.logger = logging.getLogger("API_Logger")
        self.logger.setLevel(logging.INFO)

        # Create a rotating file handler to avoid gigantic log files
        handler = RotatingFileHandler("api_calls.log", maxBytes=5000000, backupCount=5)
        handler.setLevel(logging.INFO)

        # Create a log format
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(handler)

    def log_api_call(self, method, endpoint, status_code, message=""):
        self.logger.info(f"API Call - Method: {method}, Endpoint: {endpoint}, Status Code: {status_code}, Message: {message}")