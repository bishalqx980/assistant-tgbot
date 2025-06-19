from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.decorators.sudo_users import require_sudo

@require_sudo
async def func_log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_document(open("sys/log.txt", "rb"), filename="log.txt")
