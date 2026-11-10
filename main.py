import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

NEWS = {
    "pl": "🏆 *Premier League News*\n\n• Manchester City secure a dramatic last-minute win.\n• Arsenal maintain their strong grip at the top.",
    "cl": "⭐ *Champions League News*\n\n• Real Madrid stage a classic European comeback.\n• Bayern Munich dominate their opponents.",
    "transfers": "🔄 *Transfer News*\n\n• Star midfielder linked with a move to Spain.\n• Club confirms talks for a January signing."
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Premier League", callback_data="pl"), InlineKeyboardButton("Champions League", callback_data="cl")],
        [InlineKeyboardButton("Transfer News", callback_data="transfers")]
    ]
    await update.message.reply_text("⚽ *Football News Bot*\n\nSelect a category:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("Premier League", callback_data="pl"), InlineKeyboardButton("Champions League", callback_data="cl")],
        [InlineKeyboardButton("Transfer News", callback_data="transfers")]
    ]
    
    text = NEWS.get(query.data, "News not found.")
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    app = Application.builder().token(token).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    
    app.run_polling()

if __name__ == "__main__":
    main()
