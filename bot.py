from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
import requests
from datetime import datetime, timedelta

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GOOGLE_SCRIPT_URL = os.getenv("GOOGLE_SCRIPT_URL")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт 👋\n\n"
        "Напиши:\n"
        "Створи зустріч завтра о 15:00 з Іваном"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    now = datetime.now()
    start = now + timedelta(minutes=5)
    end = start + timedelta(hours=1)

    payload = {
        "title": text,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "attendees": []
    }

    try:
        response = requests.post(GOOGLE_SCRIPT_URL, json=payload)

        if response.status_code == 200:
            data = response.json()

            await update.message.reply_text(
                f"✅ Зустріч створена!\n\n"
                f"📅 {data['title']}\n"
                f"🕒 {data['start']}\n\n"
                f"🔗 {data['link']}"
            )
        else:
            await update.message.reply_text(
                f"❌ Помилка створення зустрічі\n{response.text}"
            )

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()
