# Copyright © Michael Lohier 2024 All rights reserved.

import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from src.logger import setup_logger
from src.telegram_bot.commands import (
    COMMAND_ANSWER,
    COMMAND_CANCEL,
    COMMAND_HELP,
    COMMAND_START,
)
from src.telegram_bot.commands.answer import answer
from src.telegram_bot.commands.cancel import cancel
from src.telegram_bot.commands.help import help
from src.telegram_bot.commands.start import start
from src.telegram_bot.message_handler import handle_message

load_dotenv()
logger = setup_logger()


def main() -> None:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        logger.error("The bot token is not defined")
        return
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler(COMMAND_ANSWER, answer))
    application.add_handler(CommandHandler(COMMAND_CANCEL, cancel))
    application.add_handler(CommandHandler(COMMAND_HELP, help))
    application.add_handler(CommandHandler(COMMAND_START, start))

    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    logger.info("Bot started. Waiting for messages...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
