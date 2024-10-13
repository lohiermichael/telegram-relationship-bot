# Copyright © Michael Lohier 2024 All rights reserved.

import asyncio
import os

from telegram import Bot

from scripts.utils import load_proper_env
from src.logger import setup_logger

logger = setup_logger()


async def get_bot_group_id(bot: Bot) -> str:
    # Get updates to find the chat ID
    updates = await bot.get_updates()
    if not updates:
        logger.error("There are no updates for this bot")
        return ""
    last_message = updates[-1].message
    if last_message is None:
        logger.error("Last update has no message, try with another one")
        return ""
    bot_group_id = str(last_message.chat.id)
    logger.debug(f"Group ID: {bot_group_id}")

    return bot_group_id


async def main() -> None:
    load_proper_env()
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        logger.error("THE BOT_TOKEN environment variable has bot been set properly")
        return
    bot = Bot(token=BOT_TOKEN)
    # Get the id of the group
    bot_group_id = await get_bot_group_id(bot)
    if not bot_group_id:
        logger.error("Could not retrieve the group information")
        return

    # send a test message in the group with the bot
    await bot.send_message(chat_id=bot_group_id, text="Test message")
    logger.info("Message properly sent to the group")

    if bot_group_id:
        logger.info(f"The group id is {bot_group_id}")
    else:
        logger.error("Couln't get the group id")


if __name__ == "__main__":
    asyncio.run(main())
