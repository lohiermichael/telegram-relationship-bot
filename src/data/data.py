# Copyright © Michael Lohier 2024 All rights reserved.

import json
import os
from datetime import datetime

from src.logger import setup_logger
from src.utils import Singleton

logger = setup_logger()


class Data(metaclass=Singleton):
    def __init__(self):
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_file = os.path.join(self.root_dir, "data.json")
        self.template_file = os.path.join(self.root_dir, "data_template.json")
        self.data = self._load_data()

    def _load_data(self):
        try:
            with open(self.data_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            logger.error(
                f"Couldn't load data from {self.data_file}, creating an empty one."
            )
            return self._load_template()

    def _load_template(self):
        with open(self.template_file, "r") as f:
            data = json.load(f)
        self._save_data(data)
        return data

    def _save_data(self, data):
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=4)

    def store_last_command(self, user_id, command):
        self.data["last_command"][user_id] = {
            "command": command,
            "timestamp": datetime.now().isoformat(),
        }
        self._save_data(self.data)

    def get_last_command(self, user_id):
        return self.data["last_command"].get(user_id, {}).get("command")

    def has_last_command(self, user_id):
        return user_id in self.data["last_command"]

    def delete_last_command(self, user_id):
        if user_id in self.data["last_command"]:
            del self.data["last_command"][user_id]
            self._save_data(self.data)

    def store_response(self, user_id, response):
        """Store a user response."""
        self.data["user_responses"][user_id] = {
            "response": response,
            "timestamp": datetime.now().isoformat(),
        }
        self._save_data(self.data)

    def has_user_responded(self, user_id):
        return user_id in self.data["user_responses"]

    def get_daily_question(self):
        return self.data["daily_question"]

    def store_daily_question(self, question):
        self.data["daily_question"] = question
        self._save_data(self.data)
