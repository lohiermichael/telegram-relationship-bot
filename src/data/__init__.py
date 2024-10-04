# Copyright © Michael Lohier 2024 All rights reserved.

import json
import os
from datetime import datetime

from src.logger import setup_logger

logger = setup_logger()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(ROOT_DIR, "data.json")
DATA_TEMPLATE_FILE = os.path.join(ROOT_DIR, "data_template.json")


def _load_data():
    with open(DATA_TEMPLATE_FILE, "r") as f:
        data = json.load(f)
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logger.error(f"Couldn't load data from {DATA_FILE}, create an empty one.")
        save_data(data)
    finally:
        return data


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# Load data at startup
data = _load_data()


# To store a response
def store_response(user_id, response):
    data["user_responses"][user_id] = {
        "response": response,
        "timestamp": datetime.now().isoformat(),
    }
    save_data(data)


# To store the last command
def store_last_command(user_id, command):
    data["last_command"][user_id] = {
        "command": command,
        "timestamp": datetime.now().isoformat(),
    }
    save_data(data)


def get_data():
    return data
