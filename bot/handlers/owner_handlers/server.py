from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.database import MemoryDB, MongoDB
from bot.utils.decorators.sudo_users import require_sudo

@require_sudo
async def func_server(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    new_url = " ".join(context.args)

    server_url = MemoryDB.bot_data.get("server_url")

    if not new_url:
        await message.reply_text(f"<code>/server URL</code>\nCurrent URL: {server_url}")
        return
    
    _id = MemoryDB.bot_data.get("_id")

    response = MongoDB.update("bot_data", "_id", _id, "server_url", new_url)
    if not response:
        await message.reply_text("Something went wrong!")
        return
    
    MemoryDB.insert("bot_data", None, {"server_url": new_url})

    await message.reply_text(f"Server URL updated with: <code>{new_url}</code>")
