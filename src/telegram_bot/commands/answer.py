# Copyright © Michael Lohier 2024 All rights reserved.

import textwrap

from telegram import Update

from src.ai import AI
from src.data.data import Data, UserStatus
from src.logger import setup_logger

from . import COMMAND_ANSWER, COMMAND_START

logger = setup_logger()
data_instance = Data()

ai = AI()


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
