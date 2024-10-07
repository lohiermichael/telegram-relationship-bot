# Copyright © Michael Lohier 2024 All rights reserved.

import logging
import os


def setup_logger(log_file: str = "app.log", level: str = "INFO") -> logging.Logger:
    # Create the logger
    logger = logging.getLogger("Telegram Relationship Bot")

    # Check if logger already has handlers (prevents adding handlers multiple times)
    if logger.hasHandlers():
        return logger

    # Set the logging level dynamically based on the input
    log_level = os.getenv("LOG_LEVEL", "INFO")

    logger.setLevel(log_level)

    # Create a file handler to write log messages to a file
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)  # Always log DEBUG to file

    # Create a console handler to output log messages to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)  # Log at the selected level for the console

    # Create a formatter and set it for both handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger (if not already added)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
