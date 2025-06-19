from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.decorators.error_hunter import error_hunter

@error_hunter
async def func_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "/start - start the bot\n"
        "/help - get this message :)\n"
        "/id - get user/chat id\n"
        "/info - get user info\n\n"
        
        "Bot owner commands -\n\n"
        "/sys - get system info\n"
        "/broadcast - broadcast message to all user\n"
        "/database - get database info\n"
        "/log - for development/finding any error/bug\n"
        "/shell - use system shell\n\n"
        "<i><b>Note:</b> You can understand whether or not the message was sent by bot reaction!!</i>\n"
        "<i>The bot is compatible with the <code>/</code>, <code>!</code>, and <code>.</code> command prefixes.</i>"
    )

    await update.message.reply_text(text)
