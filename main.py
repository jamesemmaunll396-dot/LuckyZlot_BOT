import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# 1. Put your contact/DM link here (Make sure to include https://t.me/...)
DM_LINK = "https://t.me/galaxy99_kh" # <--- CHANGE THIS TO YOUR ACTUAL DM LINK

# 2. Your updated welcome message
WELCOME_MESSAGE = (
    "សូមស្វាគមន៍មកវេបសាយធំបំផុត ងាយស្រួលលេង📲 និងគួរឱ្យទុកចិត្តបំផុតនៅកម្ពុជា🔥\n"
    "សេវាកម្ម២៤ម៉ោង: https://t.me/galaxy99_kh\n\n"
    "👇 ចុចប៊ូតុងខាងក្រោមដើម្បីទទួលបានការបញ្ចុះតម្លៃ 👇" # Khmer text saying "Click the button below to get a discount"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends the welcome message with a link button when /start is issued."""
    
    # 3. Create the button
    keyboard = [
        [
            InlineKeyboardButton(
                text="💬 DM NOW TO GET FREE BONUS", 
                url=DM_LINK
            )
        ]
    ]
    
    # 4. Attach the keyboard to the message
    reply_markup = InlineKeyboardMarkup(keyboard)

    # 5. Send the message with the button
    await update.message.reply_text(
        text=WELCOME_MESSAGE, 
        reply_markup=reply_markup
    )

def main() -> None:
    """Start the bot."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    
    if not token:
        raise ValueError("No TELEGRAM_BOT_TOKEN found in environment variables.")

    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))

    application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == "__main__":
    main()
