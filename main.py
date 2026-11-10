import os
import logging
import feedparser
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# RSS Feed URLs for popular football news categories
FEEDS = {
    "pl": "https://www.skysports.com/rss/0,20514,11661,00.xml",       # Premier League
    "cl": "https://www.skysports.com/rss/0,20514,11979,00.xml",       # Champions League
    "transfers": "https://www.skysports.com/rss/0,20514,12040,00.xml", # Transfer News
}

def build_menu_keyboard():
    """Builds inline keyboard options for the user."""
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
    """Fetches and formats top news headlines from an RSS feed."""
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
    """Sends start message with options."""
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
    """Handles button presses from inline keyboards."""
    query = update.callback_query
    await query.answer()

    if query.data.startswith("news_"):
        category = query.data.replace("news_", "")
        news_content = fetch_latest_news(category)

        # Edit message content and attach keyboard again for seamless navigation
        await query.edit_message_text(
            text=news_content,
            reply_markup=build_menu_keyboard(),
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

def main() -> None:
    """Starts the bot using environment token."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable is missing.")

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Start Polling
    application.run_polling()

if __name__ == "__main__":
    main()
