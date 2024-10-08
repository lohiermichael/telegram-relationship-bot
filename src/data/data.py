# Copyright © Michael Lohier 2024 All rights reserved.

import json
import os
from datetime import datetime
from enum import Enum

from src.logger import setup_logger
from src.utils import Singleton

logger = setup_logger()


class UserStatus(Enum):
    ALLOWED = 1
    NOT_ALLOWED = 2
    NEED_TO_START = 3


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
            json.dump(data, f, indent=2)

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

    def get_number_responses(self) -> int:
        return len(self.data["user_responses"].keys())

    def has_user_responded(self, user_id):
        return user_id in self.data["user_responses"]

    def get_daily_question(self):
        return self.data["daily_question"]

    def store_daily_question(self, question):
        self.data["daily_question"] = question
        self._save_data(self.data)

    def store_user(self, user):
        self.data["users"][str(user.id)] = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
        }
        self._save_data(self.data)

    def get_user_status(self, user_id) -> UserStatus:
        if user_id in self.data["users"].keys():
            return UserStatus.ALLOWED
        if len(self.data["users"].keys()) < 2:
            return UserStatus.NEED_TO_START
        return UserStatus.NOT_ALLOWED

    def get_data_for_suggestions(self):
        data_for_suggestions = {}
        user_index = 1
        for user_id, user in self.data["users"].items():
            user_response = self.data["user_responses"][user_id]["response"]
            data_for_suggestions[f"user{user_index}_name"] = user["first_name"]
            data_for_suggestions[f"user{user_index}_response"] = user_response
            user_index += 1

        return data_for_suggestions
