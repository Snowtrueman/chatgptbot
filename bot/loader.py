import os
import logging
from db import get_session
from dotenv import load_dotenv
from telebot import TeleBot


def get_logger() -> logging.Logger:
    """
        Configures and creates logger.
    Returns:
        Logger instance.
    """

    log_directory = "logs"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    logging.basicConfig(level=logging.INFO, filename="logs/log.log", filemode="w",
                        format="%(asctime)s : %(levelname)s | %(name)s --- %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    return logging.getLogger("bot")


def load_env() -> None:
    """
    Load all the variables found as environment variables in .env file.
    Returns:
        None
    """
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")

    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    else:
        logger.critical("Missing .env file. Can't find it in project root directory.")


logger = get_logger()
session = get_session()

load_env()
TELEGRAM_TOKEN = os.environ.get("TELEGRAM-TOKEN")
OPENAPI_TOKEN = os.environ.get("OPENAPI-TOKEN")
SECRET_KEY = os.environ.get("SECRET-KEY")
bot = TeleBot(TELEGRAM_TOKEN, threaded=False)



