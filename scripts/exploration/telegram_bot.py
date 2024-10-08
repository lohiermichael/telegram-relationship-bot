# Copyright © Michael Lohier 2024 All rights reserved.

import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from src.logger import setup_logger

load_dotenv()

logger = setup_logger()


async def start(update: Update, _) -> None:
    if not update.message:
        logger.info("The update has no message")
        return
    await update.message.reply_text("Hello! I am your bot.")


async def help_command(update: Update, _) -> None:
    if not update.message:
        logger.info("The update has no message")
        return
    await update.message.reply_text("Help!")
    logger.info("Command help used")


async def handle_message(update: Update, _) -> None:
    if not update.message:
        logger.info("The update has no message")
        return
    text = update.message.text
    await update.message.reply_text(f"You said: {text}")
    logger.info(f"Message received: {text}")


def main() -> None:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        logger.error("The bot token is not defined")
        return
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    logger.info("Bot started. Waiting for messages...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
