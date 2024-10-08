# Copyright © Michael Lohier 2024 All rights reserved.

import textwrap
from typing import Dict, List, Tuple

from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_openai.chat_models import ChatOpenAI

from src.data import Data
from src.utils import Singleton

data_instance = Data()

QUESTION_TEMPLATE = textwrap.dedent(
    """
    Generate a max 50-token thoughtful question that can be asked individually
    to a man and a woman in relationship to strengthen their relationship. The
    question should be insightful and help them understand and know each other
    better. Be creative!
    """
)

SYSTEM_ROLE = """You are a couple therapist"""


class AI(metaclass=Singleton):
    def __init__(self) -> None:
        self.template_variables: Dict[str, str] = {}
        self.messages: List[Tuple[str, str]] = []
        self.model = ChatOpenAI(model="gpt-4o", max_tokens=170)

    def get_daily_question(self) -> str:
        daily_question = data_instance.get_daily_question()
        if daily_question:
            return daily_question

        daily_question = self._generate_daily_question()

        # Store the daily question
        data_instance.store_daily_question(daily_question)

        return daily_question

    def _generate_daily_question(self) -> str:
        self.template_variables.update()

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
