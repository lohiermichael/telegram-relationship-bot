# Copyright © Michael Lohier 2024 All rights reserved.
from telegram import Update

from src.data.data import Data, UserStatus
from src.logger import setup_logger

from . import COMMAND_START, HELPER

logger = setup_logger()
data_instance = Data()


async def start(update: Update, _) -> None:
    logger.info(f"Command /{COMMAND_START} used")

    if not update.message:
        logger.info("The update has no message")
        return
    user = update.message.from_user
    if not user:
        logger.error("The message user cannot be accessed")
        return
    user_id = str(user.id)
    user_status = data_instance.get_user_status(user_id)
    if user_status == UserStatus.NOT_ALLOWED:
        await update.message.reply_text("⛔ You are not authorized to use this bot. 🚫")
        return
    data_instance.store_user(user)

    await update.message.reply_text(
        f"""
        👋 Hello {user.first_name}! You have started interacting with your catherapist 🐱.
        {HELPER}
        """
    )
