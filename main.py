import os
import logging
import asyncio
import feedparser
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

FEEDS = {
    "pl": "https://www.skysports.com/rss/0,20514,11661,00.xml",       
    "cl": "https://www.skysports.com/rss/0,20514,11979,00.xml",       
    "transfers": "https://www.skysports.com/rss/0,20514,12040,00.xml", 
}

def build_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🏆 Premier League", callback_data="news_pl"),
            InlineKeyboardButton("⭐ Champions League", callback_data="news_cl"),
        ],
        [
            InlineKeyboardButton("🔄 Transfer News", callback_data="news_transfers"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def fetch_latest_news(feed_key: str, limit: int = 4) -> str:
    url = FEEDS.get(feed_key)
    if not url:
        return "Category not found."

    feed = feedparser.parse(url)
    if not feed.entries:
        return "Failed to retrieve news at the moment."

    msg = f"⚽ **Latest {feed_key.upper()} News**\n\n"
    for entry in feed.entries[:limit]:
        title = entry.get("title", "No Title")
        link = entry.get("link", "#")
        msg += f"• [{title}]({link})\n\n"

    return msg

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "Welcome to the **Football News Bot**! ⚽\n\n"
        "Select an option below to get the latest football headlines:"
    )
    await update.message.reply_text(
        text=welcome_text,
        reply_markup=build_menu_keyboard(),
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data.startswith("news_"):
        category = query.data.replace("news_", "")
        news_content = fetch_latest_news(category)

        await query.edit_message_text(
            text=news_content,
            reply_markup=build_menu_keyboard(),
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable is missing.")

    # Fix for Python 3.14 event loop initialization
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    application.run_polling()

if __name__ == "__main__":
    main()
