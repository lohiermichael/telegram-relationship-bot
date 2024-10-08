# Copyright © Michael Lohier 2024 All rights reserved.

import os
import textwrap

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from src.ai import AI
from src.data import Data
from src.logger import setup_logger

load_dotenv()
logger = setup_logger()

# Singleton instance of Data to access stored information
data_instance = Data()

# Singleton instance of the AI
ai = AI()

# Constants for command strings
COMMAND_ANSWER = "answer"
COMMAND_CANCEL = "cancel"
COMMAND_HELP = "help"

HELPER = f"""
Here are the available commands. Only these can be used to interact with the bot.

/{COMMAND_HELP} - open the helper menu
/{COMMAND_ANSWER} - answer to the question of the day
/{COMMAND_CANCEL} - cancel the previously started action (ex: /{COMMAND_ANSWER})
"""


async def help(update: Update, _) -> None:
    logger.info("Command /help used")
    if not update.message:
        logger.info("The update has no message")
        return
    await update.message.reply_text(HELPER)


async def answer(update: Update, _) -> None:
    logger.info("Command /answer used")
    if not update.message:
        logger.info("The update has no message")
        return
    user = update.message.from_user
    if not user:
        logger.error("The message user cannot be accessed")
        return
    user_id = str(user.id)

    if data_instance.has_user_responded(user_id):
        await update.message.reply_text(
            "You have already responded to the question of the day."
        )
        return

    daily_question = ai.get_daily_question()

    await update.message.reply_text(
        textwrap.dedent(
            f"""
            Hey {user.first_name},\n
            Please give your answer to the question of the day:\n
            *{daily_question}*
            """
        ),
        parse_mode="MarkdownV2",
    )

    # Store the last command used
    data_instance.store_last_command(user_id, COMMAND_ANSWER)
    logger.info(f"Last command /{COMMAND_ANSWER} stored for user {user.name}")


async def cancel(update: Update, _) -> None:
    logger.info("Command /cancel used")
    if not update.message:
        logger.info("The update has no message")
        return
    user = update.message.from_user
    if not user:
        logger.error("The message user cannot be accessed")
        return

    user_id = str(user.id)

    if not data_instance.has_last_command(user_id):
        await update.message.reply_text("No previous action to cancel.")
        return

    data_instance.delete_last_command(user_id)
    await update.message.reply_text("Your last action has been cancelled.")
    logger.info(f"Last command for user {user_id} cancelled.")


async def handle_message(update: Update, _) -> None:
    if not update.message:
        logger.info("The update has no message")
        return
    user = update.message.from_user
    if not user:
        logger.error("The message user cannot be accessed")
        return

    logger.info(f"User {user.name} input a message")

    user_id = str(user.id)

    # Check the last command issued by the user
    user_last_command = data_instance.get_last_command(user_id)
    if not user_last_command or user_last_command != COMMAND_ANSWER:
        logger.info(f"Last command was not /{COMMAND_ANSWER}")
        await update.message.reply_text(HELPER)

    # Store the user's response
    text = update.message.text
    data_instance.store_response(user_id, text)

    await update.message.reply_text(f"You said: {text}")
    logger.info(f"Response stored for user {user_id}: {text}")


def main() -> None:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        logger.error("The bot token is not defined")
        return
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler(COMMAND_ANSWER, answer))
    application.add_handler(CommandHandler(COMMAND_CANCEL, cancel))
    application.add_handler(CommandHandler(COMMAND_HELP, help))

    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    logger.info("Bot started. Waiting for messages...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
