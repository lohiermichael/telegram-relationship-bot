# Copyright © Michael Lohier 2024 All rights reserved.

import os
import re
import textwrap

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from src.ai import AI
from src.data import Data
from src.data.data import UserStatus
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
COMMAND_START = "start"

HELPER = f"""
Here are the available commands. Only these can be used to interact with the bot.

/{COMMAND_HELP} - open the helper menu
/{COMMAND_ANSWER} - answer to the question of the day
/{COMMAND_CANCEL} - cancel the previously started action (ex: /{COMMAND_ANSWER})
"""


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


async def answer(update: Update, _) -> None:
    logger.info(f"Command /{COMMAND_ANSWER} used")

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
            *{daily_question}*\n

            You need to long press this message an click on "Reply"
            """
        ),
        parse_mode="MarkdownV2",
    )

    # Store the last command used
    data_instance.store_last_command(user_id, COMMAND_ANSWER)
    logger.info(f"Last command /{COMMAND_ANSWER} stored for user {user.name}")


async def cancel(update: Update, _) -> None:
    logger.info(f"Command /{COMMAND_CANCEL} used")

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

    if not data_instance.has_last_command(user_id):
        await update.message.reply_text("No previous action to cancel.")
        return

    data_instance.delete_last_command(user_id)
    await update.message.reply_text("Your last action has been cancelled.")
    logger.info(f"Last command for user {user_id} cancelled.")


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
        await update.message.reply_text("You are not authorized to use this bot.")
        return
    data_instance.store_user(user)

    await update.message.reply_text(
        f"""
        Hello {user.first_name}! You have started interacting with the bot.

        {HELPER}
        """
    )


async def handle_message(update: Update, _) -> None:
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

    # Check the last command issued by the user
    user_last_command = data_instance.get_last_command(user_id)
    if not user_last_command or user_last_command != COMMAND_ANSWER:
        logger.info(f"Last command was not /{COMMAND_ANSWER}")
        await update.message.reply_text(HELPER)

    # Store the user's response
    text = update.message.text
    data_instance.store_response(user_id, text)
    logger.info(f"Response stored for user {user.name}: {text}")

    number_responses = data_instance.get_number_responses()
    if number_responses == 1:
        await update.message.reply_text(
            textwrap.dedent(
                """
            You are the first one to answer the question, let's wait the second
            answer to generate the suggestions
            """
            )
        )
    elif number_responses == 2:
        await update.message.reply_text(
            textwrap.dedent(
                """
            Both of your answers are gathered, the AI is gonna come up with
            suggesetions
            """
            )
        )

        suggestions = ai.get_suggestions()
        # Remove unnecessary escape characters
        suggestions = suggestions.replace("\\", "")  # Remove backslashes

        # A single * is working to make text bold
        suggestions = suggestions.replace("**", "*")
        # Escape characters for MarkdownV2
        suggestions = re.sub(r"([_[\]()~`>#+\-=|{}.!])", r"\\\1", suggestions)

        await update.message.reply_text(suggestions, parse_mode="MarkdownV2")


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
