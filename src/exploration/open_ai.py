# Copyright © Michael Lohier 2024 All rights reserved.

import os
import textwrap
from typing import List

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from src.logger import setup_logger

script_directory = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(script_directory))
load_dotenv(os.path.join(ROOT_DIR, "docker/dev/.env"))

client = OpenAI()

# Set up logging
logger = setup_logger()

# Retrieve the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    logger.error("OpenAI API key not found in environment variables.")
    raise ValueError("OpenAI API key is required")


def get_response_from_request(client: OpenAI, request: str) -> str:
    logger.debug(f"Request: {request}")
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": request,
            },
        ],
    )
    response = completion.choices[0].message.content

    if response is None:
        logger.error(f"No response to the request: {request}")
        return "No response"

    logger.debug(f"Get response: {response}")
    return response


class OpenAIConversation:

    BOT_ROLE = textwrap.dedent(
        """
        You are a relationship expert that helps couples strenghten their
        relationships.
        """
    )

    def __init__(self):
        self.messages: List[ChatCompletionMessageParam] = [
            {"role": "system", "content": [{"type": "text", "text": self.BOT_ROLE}]}
        ]

    def respond_to(self, message: str) -> str:

        self.messages.append({"role": "user", "content": message})
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=self.messages,
        )
        response = completion.choices[0].message.content

        if response is None:
            logger.error(f"No response to the message: {message}")
            return "No response"

        logger.debug(f"Get response: {response}")
        self.messages.append(
            {"role": "assistant", "content": [{"type": "text", "text": response}]}
        )
        return response


def main() -> None:
    logger.info("The conversation starts...")
    conversation = OpenAIConversation()
    while True:
        message = input("Type your request: ")
        response = conversation.respond_to(message)
        logger.info(response)


if __name__ == "__main__":
    main()
