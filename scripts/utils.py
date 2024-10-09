import argparse
import os

from dotenv import load_dotenv

script_directory = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(script_directory)


def load_proper_env() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", type=str)
    args = parser.parse_args(None)
    env_path = os.path.join(ROOT_DIR, f"docker/{args.env}/.env")
    load_dotenv(env_path)
