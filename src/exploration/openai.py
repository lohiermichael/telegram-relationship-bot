# Copyright © Michael Lohier 2024 All rights reserved.

import os

from dotenv import load_dotenv
from openai import OpenAI

from src.logger import setup_logger

load_dotenv()

# Set up logging
logger = setup_logger()


def main() -> None:
    # Retrieve the OpenAI API key from environment variables
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    if not OPENAI_API_KEY:
        logger.error("OpenAI API key not found in environment variables.")
        raise ValueError("OpenAI API key is required")

    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "Write a short sentence with advice to find love",
            },
        ],
    )

    print(completion.choices[0].message)


if __name__ == "__main__":
    main()
