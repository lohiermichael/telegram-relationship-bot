import re


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def format_markdown_v2(message: str) -> str:
    # Remove unnecessary escape characters
    message = message.replace("\\", "")  # Remove backslashes

    # A single * is working to make text bold
    message = message.replace("**", "*")
    # Escape characters for MarkdownV2
    message = re.sub(r"([_[\]()~`>#+\-=|{}.!])", r"\\\1", message)

    return message
