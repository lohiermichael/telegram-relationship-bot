# Copyright © Michael Lohier 2024 All rights reserved.

import textwrap

from dotenv import load_dotenv
from telegram.ext import Application

from src.ai import AI
from src.logger import setup_logger
from src.telegram_bot.commands import COMMAND_ANSWER
from src.utils import format_markdown_v2

load_dotenv()
logger = setup_logger()

ai = AI()


async def send_scheduled_message(application: Application, group_id: str) -> None:
    daily_question = ai.get_daily_question()

    message = textwrap.dedent(
        f"""
        Hey lovers,
        Here is the question of the day:

        *{daily_question}*

        Feel free to give your answer to this question by typing the
        /{COMMAND_ANSWER} command.
        """
    )

    message = format_markdown_v2(message)

    logger.debug(message)

    await application.bot.send_message(
        chat_id=group_id, text=message, parse_mode="MarkdownV2"
    )
    logger.info(f"Sending scheduled message to group {group_id}")
