from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт 👋\nНапиши задачу для зустрічі.\n\nНаприклад:\nСтвори зустріч завтра о 15:00 з Іваном"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    response = f"""
✅ Запит отримано

Текст:
{text}

🤖 Тут буде AI-аналіз:
- учасники
- дата
- час
- створення meeting
"""

    await update.message.reply_text(response)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
