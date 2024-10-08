# Copyright © Michael Lohier 2024 All rights reserved.

# Constants for command strings
COMMAND_ANSWER = "answer"
COMMAND_CANCEL = "cancel"
COMMAND_HELP = "help"
COMMAND_START = "start"

HELPER = f"""
Here are the available commands. Only these can be used to interact with the bot.

/{COMMAND_START} - start interacting with the bot
/{COMMAND_HELP} - open the helper menu
/{COMMAND_ANSWER} - answer to the question of the day
/{COMMAND_CANCEL} - cancel the previously started action (ex: /{COMMAND_ANSWER})
"""
