# Copyright © Michael Lohier 2024 All rights reserved.

import textwrap
from typing import Dict, List, Tuple

from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_openai.chat_models import ChatOpenAI

from src.data import Data
from src.logger import setup_logger
from src.utils import Singleton

data_instance = Data()

logger = setup_logger()

QUESTION_TEMPLATE = textwrap.dedent(
    """
    Here is a basic question to ask individually to a man and a woman in
    relationship:

    {common_question}

    Improve it and keep short under 50 tokens!
    """
)

SYSTEM_ROLE = """You are a couple therapist"""

RESPONSE_TEMPLATE = textwrap.dedent(
    """
    Here are two responses to the question:
    - {user1_name}'s response: {user1_response}
    - {user2_name}'s response: {user2_response}

    Based on these responses, provide suggestions in maximum 150 tokens on
    how they can strengthen their relationship with original and concreate
    actions. Add smileys to your response.
    """
)


class AI(metaclass=Singleton):
    def __init__(self) -> None:
        self.template_variables: Dict[str, str] = {}
        self.messages: List[Tuple[str, str]] = []
        self.model = ChatOpenAI(model="gpt-4o", max_tokens=200)

    def get_daily_question(self) -> str:
        daily_question = data_instance.get_daily_question()
        if daily_question:
            return daily_question

        daily_question = self._generate_daily_question()

        # Store the daily question
        data_instance.store_daily_question(daily_question)

        return daily_question

    def _generate_daily_question(self) -> str:
        common_question = data_instance.get_common_question()
        self.template_variables.update({"common_question": common_question})
        data_instance.increment_common_question_index()

        self.messages = [
            ("system", SYSTEM_ROLE),
            ("human", QUESTION_TEMPLATE),
        ]

        message_template = ChatPromptTemplate.from_messages(self.messages)

        chain = message_template | self.model | StrOutputParser()
        daily_question = chain.invoke(self.template_variables)

        # Store the daily message in the messages
        self.messages.append(("ai", daily_question))

        return daily_question

    def get_suggestions(self) -> str:
        self.messages.append(("human", RESPONSE_TEMPLATE))

        # Get data from storage
        users_info = data_instance.get_data_for_suggestions()
        self.template_variables.update(users_info)

        message_template = ChatPromptTemplate.from_messages(self.messages)

        chain = message_template | self.model | StrOutputParser()
        suggestions = chain.invoke(self.template_variables)

        data_instance.store_suggestions(suggestions)

        return suggestions
