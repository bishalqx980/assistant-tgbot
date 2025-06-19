from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.decorators.error_hunter import error_hunter

@error_hunter
async def func_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "<blockquote>Command's list</blockquote>"
        "• /start - Start the bot\n"
        "• /help - Get this message 😝\n"
        "• /id - Get User/Chat ID\n"
        "• /info - Get user info\n\n"
        
        "<b>Owner only</b>\n\n"
        "• /broadcast - Broadcast message to all users\n"
        "• /database - Get database info\n"
        "• /log - Get log file (development/finding any error/bug)\n"
        "• /say - Say something as bot\n"
        "• /shell - Use shell og hosted server/own PC/device\n"
        "• /sys - Get system info"
    )

    await update.message.reply_text(text)
