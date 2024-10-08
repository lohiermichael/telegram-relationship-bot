# Copyright © Michael Lohier 2024 All rights reserved.

import asyncio
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv
from telegram import Bot

from src.logger import setup_logger

script_directory = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(script_directory))
load_dotenv(os.path.join(ROOT_DIR, "docker/dev/.env"))

logger = setup_logger()


async def scheduled_task():
    """A simple scheduled task that prints the current time."""
    logger.info("Task executed")


async def send_message_to_chat(bot: Bot, chat_id: str) -> None:
    await bot.send_message(chat_id=chat_id, text="Test message")
    logger.info("Message properly sent to the group")


async def main() -> None:
    # Create the bot
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        logger.error("THE BOT_TOKEN environment variable has bot been set properly")
        return
    bot = Bot(token=BOT_TOKEN)

    GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")
    if not GROUP_CHAT_ID:
        logger.error("THE GROUP_CHAT_ID environment variable has bot been set properly")
        return

    # Create an AsyncIOScheduler instance
    scheduler = AsyncIOScheduler()

    # Add a job to the scheduler - runs every 10 seconds for demonstration
    # scheduler.add_job(scheduled_task, trigger='interval', seconds=2)

    # Alternatively, you can schedule a job to run every day at a specific time
    scheduler.add_job(
        send_message_to_chat, CronTrigger(hour=19, minute=36), args=[bot, GROUP_CHAT_ID]
    )

    # Start the scheduler
    scheduler.start()
    logger.info("The scheduler started")

    # Keep the main function running to allow the scheduled tasks to execute
    try:
        while True:
            await asyncio.sleep(1)  # Keep the event loop running
    except (KeyboardInterrupt, SystemExit):
        pass


# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
