# Copyright © Michael Lohier 2024 All rights reserved.

from telegram import Update

from src.data.data import Data, UserStatus
from src.logger import setup_logger

from . import COMMAND_HELP, COMMAND_START, HELPER

logger = setup_logger()

data_instance = Data()


async def help(update: Update, _) -> None:
    logger.info(f"Command /{COMMAND_HELP} used")

    if not update.message:
        logger.info("The update has no message")
        return
    user = update.message.from_user
    if not user:
        logger.error("The message user cannot be accessed")
        return
    user_id = str(user.id)
    user_status = data_instance.get_user_status(user_id)
    if user_status == UserStatus.NEED_TO_START:
        await update.message.reply_text(
            f"You need to type /{COMMAND_START} to start using the bot"
        )
        return
    if user_status == UserStatus.NOT_ALLOWED:
        await update.message.reply_text("You are not authorized to use this bot.")
        return

    await update.message.reply_text(HELPER)
