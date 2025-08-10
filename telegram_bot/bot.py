from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from Modules import bot_token, mongo_uri
import secrets
from datetime import datetime, timezone
from pymongo import MongoClient

MONGODB_URI = mongo_uri.get_mongo_uri()
if not MONGODB_URI:
    raise ValueError("Missing MONGODB_URI in mongo_uri module")

client = MongoClient(MONGODB_URI)
db = client["pc_verification"]
collection = db["users"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🖥️💡 **PC LOGIN ALERT** 💡🖥️\n\n"
        "🔐 *Welcome!* We help you find out **who is using your PC** 👀\n\n"
        "⚡ To get your unique verification code (UID) and secure your system, "
        "please type:\n\n"
        "👉 `/verify`\n\n"
        "🛡️ Stay safe. Stay in control!"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    username = update.effective_chat.username or f"user_{chat_id}"

    captcha = secrets.token_hex(4)

    try:
        collection.update_one(
            {"username": username},
            {
                "$set": {
                    "chat_id": chat_id,
                    "username": username,
                    "code": captcha,
                    "created_at": datetime.now(timezone.utc)
                }
            },
            upsert=True
        )
    except Exception as e:
        await update.message.reply_text(f"⚠️ Database error: {e}")
        return

    await update.message.reply_text(
        f"🔑 **Your verification code is:**\n\n`{captcha}`\n\n"
        f"📌 Your username: `{username}`\n"
        "Enter these in your PC application to complete verification.",
        parse_mode="Markdown"
    )

def main():
    app = ApplicationBuilder().token(bot_token.get_bot_token()).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("verify", verify))
    app.run_polling()

if __name__ == "__main__":
    main()
