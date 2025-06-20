import asyncio
import aiohttp
import traceback

from telegram import Update, LinkPreviewOptions, BotCommand
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    ChatMemberHandler,
    Defaults
)
from telegram.constants import ParseMode
from telegram.error import BadRequest

from . import DEFAULT_ERROR_CHANNEL_ID, RUN_SERVER, bot, logger, config
from .utils.alive import alive
from .utils.update_db import update_database
from .utils.database import MemoryDB

from .handlers import (
    func_start,
    func_help,

    func_broadcast,
    func_database,
    func_log,
    func_say,
    func_send,
    func_server,
    func_shell,
    func_sys,

    func_id,
    func_info,

    func_filterAll
)

from .utils.other.bot_chats_tracker import bot_chats_tracker


async def post_init():
    try:
        await bot.set_my_commands([
            BotCommand("start", "Introducing..."),
            BotCommand("help", "Bots help section...")
        ])
    except Exception as e:
        logger.error(e)

    # Send alive message to bot owner
    try:
        await bot.send_message(config.owner_id, "<blockquote><b>Bot Started!</b></blockquote>", parse_mode=ParseMode.HTML)
    except Exception as e:
        logger.error(e)
    
    logger.info("Bot Started...")


async def server_alive():
    # executing after updating database so getting data from memory...
    if not RUN_SERVER:
        return
    
    server_url = MemoryDB.bot_data.get("server_url")
    if not server_url:
        logger.warning("'Server URL' wasn't found. Bot may fall asleep if deployed on Render (free instance)")
        return
    
    while True:
        # everytime check if there is new server_url
        server_url = MemoryDB.bot_data.get("server_url")
        if not server_url:
            return
        if server_url[0:4] != "http":
            server_url = f"http://{server_url}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(server_url) as response:
                    if not response.ok:
                        logger.warning(f"{server_url} is down or unreachable. ❌ - code - {response.status}")
        except Exception as e:
            logger.error(f"{server_url} > {e}")
        await asyncio.sleep(180) # 3 min


async def default_error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(context.error)

    error_text = "".join(traceback.format_exception(type(context.error), context.error, context.error.__traceback__))
    # Remove excessive path details for readability
    error_text = "\n".join(line for line in error_text.split("\n") if "site-packages" not in line)
    # telegram message limit ?
    error_text = error_text[-2000:]

    text = (
        "<blockquote>An error occured</blockquote>\n\n"

        f"<b>• Type:</b> <code>{type(context.error).__name__}</code>\n"
        f"<b>• Message:</b> <code>{str(context.error)}</code>\n"
        "<b>• Traceback:</b>\n\n"
        f"<pre>{error_text}</pre>"
    )
    
    if DEFAULT_ERROR_CHANNEL_ID:
        try:
            await context.bot.send_message(DEFAULT_ERROR_CHANNEL_ID, text)
            return
        except BadRequest:
            pass
        except Exception as e:
            logger.error(e)
            return
    # if not DEFAULT_ERROR_CHANNEL_ID or BadRequest
    try:
        await context.bot.send_message(config.owner_id, text)
    except Exception as e:
        logger.error(e)


def main():
    default_param = Defaults(
        parse_mode=ParseMode.HTML,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
        block=False,
        allow_sending_without_reply=True
    )

    application = ApplicationBuilder().token(config.bot_token).defaults(default_param).build()

    main_handlers = [
        CommandHandler("start", func_help, filters.Regex("help")), # this need to register before main start handler
        # core func
        CommandHandler("start", func_start),
        CommandHandler("help", func_help),
        # owner func
        CommandHandler("broadcast", func_broadcast),
        CommandHandler("database", func_database),
        CommandHandler("log", func_log),
        CommandHandler("say", func_say),
        CommandHandler("send", func_send),
        CommandHandler("server", func_server),
        CommandHandler("shell", func_shell),
        CommandHandler("sys", func_sys),
        # user func
        CommandHandler("id", func_id),
        CommandHandler("info", func_info)
    ]

    # main handlers register
    application.add_handlers(main_handlers)
    # Bot chat tracker (PRIVATE: only if bot is blocked or unblocked;)
    application.add_handler(ChatMemberHandler(bot_chats_tracker, ChatMemberHandler.MY_CHAT_MEMBER))
    # filterALL : Core for this bot
    application.add_handler(MessageHandler(filters.ALL, func_filterAll))
    # Check Updates
    application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)


async def app_init():
    if RUN_SERVER:
        alive() # Server breathing
    # maintain the sequence
    update_database()
    await post_init()
    await server_alive()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(app_init())
    loop.create_task(main())
    loop.run_forever()
