import os
from dotenv import load_dotenv

load_dotenv()

YANDEX_METRIKA_TOKEN = os.getenv("YANDEX_METRIKA_TOKEN")
YANDEX_METRIKA_COUNTER_ID = os.getenv("YANDEX_METRIKA_COUNTER_ID")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
LANDING_PATH = os.getenv("LANDING_PATH")
