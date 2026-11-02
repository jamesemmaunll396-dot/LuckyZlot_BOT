import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging to see errors in Render logs
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Your exact welcome message
WELCOME_MESSAGE = (
    "សូមស្វាគមន៍មកវេបសាយធំបំផុត ងាយស្រួលលេង📲 និងគួរឱ្យទុកចិត្តបំផុតនៅកម្ពុជា🔥\n"
    "សេវាកម្ម២៤ម៉ោង: https://t.me/galaxy99_kh"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends the welcome message when /start is issued."""
    # reply_text is safer than just send_message as it works in groups too
    await update.message.reply_text(WELCOME_MESSAGE)

def main() -> None:
    """Start the bot."""
    # Render will pass the token via Environment Variables for security
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    
    if not token:
        raise ValueError("No TELEGRAM_BOT_TOKEN found in environment variables.")

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    # Register the /start command handler
    application.add_handler(CommandHandler("start", start))

    # Run the bot until the user presses Ctrl-C (or Render stops it)
    # drop_pending_updates=True prevents the bot from replying to old /starts
    # that happened while the bot was offline (common on free tiers)
    application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == "__main__":
    main()
