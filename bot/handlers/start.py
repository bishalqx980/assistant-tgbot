from telegram import Update
from telegram.ext import ContextTypes
from bot import config
from bot.utils.database import database_add_user
from bot.utils.decorators.error_hunter import error_hunter

@error_hunter
async def func_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    owner_data = await context.bot.get_chat(config.owner_ida)

    text = (
        f"Hello! I'm the assistant of @{owner_data.username}.\n"
        f"Feel free to send me a message, and I'll make sure my boss gets it. 😊\n\n"
        f"Interested in creating an assistant like me?\n"
        f"- Check out the <a href='https://github.com/bishalqx980/assistant-tgbot/'>Source Code</a>.\n\n"
        f"Looking for a feature-rich group management bot?\n"
        f"- Take a look at @MissCiri_bot or explore the <a href='https://github.com/bishalqx980/tgbot/'>Source Code</a>.\n\n"
        "<i><b>Note:</b> You can understand whether or not the message was sent by bot reaction!!</i>"
    )

    await update.message.reply_text(text)
    await database_add_user(update.effective_user)
