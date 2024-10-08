# Copyright © Michael Lohier 2024 All rights reserved.
import asyncio
import os

from dotenv import load_dotenv
from telegram import Bot

from src.logger import setup_logger

script_directory = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(script_directory))
load_dotenv(os.path.join(ROOT_DIR, "docker/prod/.env"))

logger = setup_logger()


async def get_bot_group_id(bot: Bot) -> str:
    # Get updates to find the chat ID
    updates = await bot.get_updates()
    last_message = updates[-1].message
    if last_message is None:
        logger.error("Last update has no message, try with another one")
        return ""
    logger.debug(__import__("pprint").pprint(last_message.chat.to_json()))
    bot_group_id = str(last_message.chat.id)
    logger.debug(f"Group ID: {bot_group_id}")

    return bot_group_id


async def main() -> None:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        logger.error("THE BOT_TOKEN environment variable has bot been set properly")
        return
    bot = Bot(token=BOT_TOKEN)
    # Get the id of the group
    bot_group_id = await get_bot_group_id(bot)

    # send a test message in the group with the bot
    breakpoint()
    await bot.send_message(chat_id=bot_group_id, text="Test message")
    logger.info("Message properly sent to the group")


if __name__ == "__main__":
    asyncio.run(main())
