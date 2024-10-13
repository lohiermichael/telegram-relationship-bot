# Development Setup

This guide will help you set up the **Telegram Relationship Bot** for local
development.

## Prerequisites

Make sure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python 3.12](https://www.python.org/downloads/)

## Clone the Repository

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/yourusername/telegram-relationship-bot.git
cd telegram-relationship-bot
```

## Set Up a local development environment

A **virtual environment (venv)** is recommended to manage project dependencies
in isolation from your system Python installation for developing the application
locally and commit with git.

1. Create a Virtual Environment

    Navigate to the project directory where the repository is located and
    create a virtual environment:

    ```bash
    python -m venv venv
    ```

1. Activate the Virtual Environment

    To activate the virtual environment, run the following command:

    - On macOS/Linux:

      ```bash
      source venv/bin/activate
      ```

    - On Windows:

      ```bash
      venv\Scripts\activate
      ```

1. Install Project Dependencies

    With the virtual environment activated, install the project development
    dependencies using the following command:

    ```bash
    pip install -r docker/dev/requirements.txt
    ```

1. Setup `pre-commit` for Code Quality

    To maintain code quality and ensure consistency in your project, you can
    set up pre-commit hooks. These hooks run automatically before each commit
    to check your code for common issues like linting errors, formatting, and
    security vulnerabilities.

    Run the following command to install the hooks:

    ```bash
    pre-commit install
    ```

After that you should be ready to commit with git and contribute to the project.


## Setup Telegram

1. Copy the `.env.example` file

   First, copy the `docker/dev/.env.example` file to `docker/dev/.env`:
   ```bash
   cp docker/dev/.env.example docker/dev/.env
   ```

1. Create a Telegram bot

    - Go to Telegram and search for the BotFather.

    - Start a chat with BotFather and use the /newbot command to create a new bot.

    - Follow the instructions to name your bot and choose a username.

    - After completing these steps, BotFather will provide you with a bot token.
    Save the bot_token by opening the `.env` file in the `docker/dev/ directory`
    and paste the bot token you received from BotFather after `BOT_TOKEN`.

    - Edit the bot commands as follow by going in the bot settings with:
    ```
    help - open the helper menu
    answer - answer the question of the day
    cancel - cancel the previous action
    start - start the bot
    ```

    - (Optional) You can customize the bot by adding it a description and a
    profile picture like
    <a
        href="https://github.com/lohiermichael/telegram-relationship-bot/blob/master/img/catherapist.jpeg"
        target="_blank">
            this one
    </a>.


1. Create a Group and Add the Bot to it:

    - Open Telegram and create a new group.

    - Add your bot to the group as a participant.

    - Write a message in the group to ensure the bot can receive updates.

    - Run the following Python script to get the group chat id of the group:

    ```bash
    PYTHONPATH=. python scripts/telegram/group.py --env dev
    ```

    - Save the group chat id by opening the `.env` file in the `docker/dev/`
      directory and paste the id given the script after `GROUP_CHAT_ID`.

    - (Optional) You can customize the group by adding it a description and a
    profile picture like
    <a
        href="https://github.com/lohiermichael/telegram-relationship-bot/blob/master/img/pookies_in_love_group.jpeg"
        target="_blank">
            this one
    </a>.

## Setup OpenAI

1. Follow the steps of
   <a href="https://www.youtube.com/watch?v=eRWZuijASuU" target="_blank"> this video</a>
   to get yourself an OPENAI API key.

1. Save the OPENAI API key by opening the .env file in the docker/dev/
   directory and paste the key after `GROUP_CHAT_ID`.

## Launch the environment

To start the environment, run the following command:

```bash
docker compose -f docker/dev/docker-compose.yaml up --build
```

The environment is set up to automatically reload when any Python file is
updated. This is achieved using
[watchmedo](https://github.com/gorakhargosh/watchdog), a tool that monitors
file changes and triggers reloading of the relevant processes.

With watchmedo running in the background, whenever you make changes to a Python
file, the services in the container will automatically detect the changes and
reload, ensuring your development environment stays up-to-date.
