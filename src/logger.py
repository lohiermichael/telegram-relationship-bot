# Copyright © Michael Lohier 2024 All rights reserved.
import logging


def setup_logger(log_file: str="app.log") -> logging.Logger:
    # Create the logger
    logger = logging.getLogger("Telegram Relashionship bot")
    logger.setLevel(logging.DEBUG)  # Set the logging level

    # Create a file handler to write log messages to a file
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    # Create a console handler to output log messages to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Change this to DEBUG to see all logs in console

    # Create a formatter and set it for both handlers
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Example usage
if __name__ == "__main__":
    log = setup_logger()
    log.info("Logging setup complete.")

