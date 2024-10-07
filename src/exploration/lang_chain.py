# Copyright © Michael Lohier 2024 All rights reserved.

import os
import textwrap

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai.chat_models import ChatOpenAI

from src.logger import setup_logger

script_directory = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(script_directory))
load_dotenv(os.path.join(ROOT_DIR, "docker/dev/.env"))

logger = setup_logger()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("The OPENAI_API_KEY couldn't be loaded")


def main() -> None:

    model = ChatOpenAI(model="gpt-4o", max_tokens=150)

    # Step 1: Generate a relationship-strengthening question
    man_name = "Michael"
    woman_name = "Katya"
    question_prompt = textwrap.dedent(
        f"""
        Generate a max 50-token thoughtful question that a man named {man_name}
        and a woman named {woman_name} in relationship can both answer to
        strengthen our relationship. The question should be insightful and help
        us understand each other better.
        """
    )
    messages = [
        SystemMessage(content="You're an assistant who's good at relationship"),
        HumanMessage(content=question_prompt),
    ]

    result = model.invoke(messages)
    logger.info("Result:")
    logger.info(result.content)

    messages.append(AIMessage(content=result.content))

    # Assuming you and your girlfriend provide answers, you can pass those into
    # the conversation next. For the sake of the example, let's use some sample
    # answers:
    man_answer = input("Enter man answer: ")
    woman_answer = input("Enter woman answer: ")

    # Step 2: Provide answers and ask for suggestions
    responses_prompt = textwrap.dedent(
        f"""
        Here are two answers to the question:
        - {man_name}'s answer: {man_answer}
        - {woman_name}'s answer: {woman_answer}

        Based on these responses, provide suggestions in maximum 150 tokens on
        how they can strengthen their relationship with concreate actions.
        """
    )

    messages.append(HumanMessage(content=responses_prompt))

    suggestions = model.invoke(messages)
    logger.info("Suggestions:")
    logger.info(suggestions.content)


if __name__ == "__main__":
    main()
