# Copyright © Michael Lohier 2024 All rights reserved.

import os
import textwrap

from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
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
    template_variables = {"man_name": "Michael", "woman_name": "Katya"}

    question_template = textwrap.dedent(
        """
        Generate a max 50-token thoughtful question that a man named {man_name}
        and a woman named {woman_name} in relationship can both answer to
        strengthen our relationship. The question should be insightful and help
        us understand each other better.
        """
    )

    messages = [
        ("system", "You are an assistant who is good at relationship"),
        ("human", question_template),
    ]

    message_template = ChatPromptTemplate.from_messages(messages)

    chain = message_template | model | StrOutputParser()
    ai_response = chain.invoke(template_variables)

    logger.info("Result:")
    logger.info(ai_response)

    if not isinstance(ai_response, str):
        logger.info(
            f"The response {ai_response} generated by the AI is not of type str"
        )
        return

    messages.append(("ai", ai_response))

    # Assuming you and your girlfriend provide answers, you can pass those into
    # the conversation next. For the sake of the example, let's use some sample
    # answers:
    man_answer = input("Enter man answer: ")
    woman_answer = input("Enter woman answer: ")

    # Step 2: Provide answers and ask for suggestions
    responses_template = textwrap.dedent(
        """
        Here are two answers to the question:
        - {man_name}'s answer: {man_answer}
        - {woman_name}'s answer: {woman_answer}

        Based on these responses, provide suggestions in maximum 150 tokens on
        how they can strengthen their relationship with concreate actions.
        """
    )

    messages.append(("human", responses_template))
    template_variables.update({"man_answer": man_answer, "woman_answer": woman_answer})

    message_template = ChatPromptTemplate.from_messages(messages)

    chain = message_template | model | StrOutputParser()
    suggestions = chain.invoke(template_variables)

    logger.info("Suggestions:")
    logger.info(suggestions)


if __name__ == "__main__":
    main()
