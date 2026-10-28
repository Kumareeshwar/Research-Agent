# Telegram bot. Receives a message, sends it to the API, replies with the answer.
import os
import httpx
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

load_dotenv()
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text
    await update.message.reply_text("Researching...")

    try:
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(f"{API_URL}/ask", json={"question": question})
        await update.message.reply_text(response.json()["answer"])
    except Exception as error:
        print("Error:", error)
        await update.message.reply_text("Sorry, something went wrong. Please try again.")


app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    app.run_polling()
