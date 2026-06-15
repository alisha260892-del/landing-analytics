from agents.orchestrator import run_weekly_report
from telegram_bot import send_message, send_photo
from config import LANDING_PATH


def main():
    report, chart = run_weekly_report(LANDING_PATH)
    send_message(report)
    send_photo(chart)


if __name__ == "__main__":
    main()
