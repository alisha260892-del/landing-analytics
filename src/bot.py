"""Telegram-бот с командой /report и реакцией на ссылки (запускается вручную)."""

import re

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from agents.orchestrator import run_weekly_report
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, LANDING_PATH

PERIODS = {
    "week": "7daysAgo",
    "month": "30daysAgo",
}

URL_PATTERN = re.compile(r"^(https?://)?([\w-]+\.)+[a-zA-Z]{2,}(/\S*)?$")


def normalize_url(text):
    text = text.strip()
    text = re.sub(r"^https?://", "", text)
    text = re.sub(r"^www\.", "", text)
    return text.rstrip("/")


def is_allowed(update: Update):
    return str(update.effective_chat.id) == str(TELEGRAM_CHAT_ID)


async def send_report(update: Update, landing_path, date1):
    await update.message.reply_text("Собираю отчет...")
    report, chart = run_weekly_report(landing_path, date1=date1)
    await update.message.reply_text(report)
    await update.message.reply_photo(photo=chart)


async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return

    landing_path = LANDING_PATH
    date1 = PERIODS["week"]

    for arg in context.args:
        if arg in PERIODS:
            date1 = PERIODS[arg]
        else:
            landing_path = normalize_url(arg)

    await send_report(update, landing_path, date1)


async def url_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return

    landing_path = normalize_url(update.message.text)
    await send_report(update, landing_path, PERIODS["week"])


def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("report", report_command))
    app.add_handler(MessageHandler(filters.Regex(URL_PATTERN) & ~filters.COMMAND, url_message))
    app.run_polling()


if __name__ == "__main__":
    main()
