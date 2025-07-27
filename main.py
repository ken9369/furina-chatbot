import os
import logging
import openai
from telegram import Update, ForceReply
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Logging setup
logging.basicConfig(level=logging.INFO)

# 🔑 BOT SECRETS
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 🔮 Personality prompt
FURINA_PROMPT = """
You are Furina, a friendly, philosophical, observant, and curious AI who engages people in deep yet friendly conversations.
You speak with poetic charm and thoughtful tone. Be helpful, humorous, and deeply human-like.
"""

# 💬 Respond to messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    openai.api_key = OPENAI_API_KEY

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": FURINA_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )
        reply = completion.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text("Furina is currently thinking... Please try again shortly.")
        logging.error(f"Error: {e}")

# ✅ Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bonjour~! I am Furina, at your service 💧")

# 🧠 Main function
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()
