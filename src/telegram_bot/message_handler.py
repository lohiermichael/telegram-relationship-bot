# Copyright © Michael Lohier 2024 All rights reserved.

import textwrap

from telegram import Update

from src.ai import AI
from src.data.data import Data, UserStatus
from src.logger import setup_logger
from src.utils import format_markdown_v2

from .commands import COMMAND_ANSWER, COMMAND_START, HELPER

logger = setup_logger()

data_instance = Data()

ai = AI()


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
            f"You need to type /{COMMAND_START} to start interacting with me 🚀"
        )
        return
    if user_status == UserStatus.NOT_ALLOWED:
        await update.message.reply_text("⛔ You are not authorized to use this bot. 🚫")
        return

    # Check the last command issued by the user
    user_last_command = data_instance.get_last_command(user_id)
    if not user_last_command or user_last_command != COMMAND_ANSWER:
        logger.info(f"Last command was not /{COMMAND_ANSWER}")
        await update.message.reply_text(HELPER)
        return

    # Store the user's response
    text = update.message.text
    data_instance.store_response(user_id, text)
    logger.info(f"Response stored for user {user.name}: {text}")

    number_responses = data_instance.get_number_responses()
    if number_responses == 1:
        await update.message.reply_text(
            textwrap.dedent(
                """
                🎉 You are the first one to answer the question! Let's wait for the
                second answer, and then I'll share my thoughts with you. 🕒
                """
            )
        )
    elif number_responses == 2:
        await update.message.reply_text(
            textwrap.dedent(
                """
                ✅ Both of your answers are gathered! Here are my suggestions... 💡
                """
            )
        )

        suggestions = ai.get_suggestions()
        suggestions = format_markdown_v2(suggestions)

        await update.message.reply_text(suggestions, parse_mode="MarkdownV2")

        # Save the full data in history
        data_instance.save_for_history()

        # Flush the question of the day and the user_responses for the next day
        data_instance.flush_for_next_day()

    # It was /answer before now it's back to empty
    data_instance.delete_last_command(user_id)
