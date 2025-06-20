from telegram import Update
from telegram.ext import ContextTypes
from bot import config
from bot.helpers import BuildKeyboard
from bot.utils.database import database_add_user

async def func_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    owner_data = await context.bot.get_chat(config.owner_id)

    text = (
        f"Hello! I'm the assistant of {owner_data.mention_html()}!\n"
        f"Feel free to send me a message, and I'll make sure my boss gets it. 😊\n\n"
        "<i><b>Note:</b> You can understand whether or not the message was sent by bot reaction!!</i>"
    )

    btn_data = [
        {"Source Code": "https://github.com/bishalqx980/assistant-tgbot", "Developer": "https://t.me/bishalqx680/22"},
        {"Looking for Group Management bot?": "https://t.me/MissCiri_bot?start=_tgr_pg2AbehhNDJl"}
    ]

    btn = BuildKeyboard.ubutton(btn_data)

    await update.message.reply_text(text, reply_markup=btn)
    database_add_user(update.effective_user)
